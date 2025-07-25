import logging
import io
from operator import index
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Exists, OuterRef
from django.contrib import messages
from django.http import HttpResponse
from django.utils.text import slugify
import polars as pl
from datetime import datetime
from django.http import HttpRequest
from io import BytesIO
from django.utils import timezone

from expenses.models import Category, Expense
from .forms import ListForm, ListEntryForm, ListImportForm
from .models import List, ListEntry
from users.models import User
from contacts.models import Contact

logger = logging.getLogger(__name__)


@login_required
def list_summary(request: HttpRequest):
    """
    Render the list summary page showing all lists with their statistics.
    """
    filter_type = request.GET.get("filter")

    # Get base queryset
    base_queryset = List.objects.filter(is_deleted=False)

    # Annotate all lists with expense information
    all_lists = base_queryset.annotate(
        has_expense_entries=Exists(
            ListEntry.objects.filter(list=OuterRef("pk"), is_deleted=False, associated_expense__isnull=False)
        )
    ).order_by("name")

    # Apply filters
    if filter_type == "with_expenses":
        lists = all_lists.filter(has_expense_entries=True)
    elif filter_type == "without_expenses":
        lists = all_lists.filter(has_expense_entries=False)
    else:
        lists = all_lists

    # Calculate counts for filter badges
    total_lists = all_lists.count()
    lists_with_expenses_count = all_lists.filter(has_expense_entries=True).count()
    lists_without_expenses_count = all_lists.filter(has_expense_entries=False).count()

    form = ListImportForm()
    add_list_form = ListForm()

    import_required_fields = [
        ("list_name", "Name of the list"),
        ("item", "Item name"),
    ]
    import_optional_fields = [
        ("description", "Item description"),
        ("vendor", "Vendor/Contact name"),
        ("is_completed", "TRUE/FALSE"),
        ("quantity", "Quantity (default 1)"),
        ("unit_price", "Unit price (default 0.00)"),
        ("additional_price", "Additional price regardless of quantity (default 0.00)"),
        ("expense", "Associated Expense/Budget item"),
    ]

    return render(
        request,
        "list/list_summary.html",
        {
            "lists": lists,
            "form": form,
            "add_list_form": add_list_form,
            "import_required_fields": import_required_fields,
            "import_optional_fields": import_optional_fields,
            "filter_type": filter_type,
            "total_lists": total_lists,
            "lists_with_expenses_count": lists_with_expenses_count,
            "lists_without_expenses_count": lists_without_expenses_count,
        },
    )


@login_required
def list_create(request: HttpRequest):
    """
    Creates a new list.
    """
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            list_obj = form.save(commit=False)
            list_obj.created_by = request.user
            list_obj.save()

            messages.success(request, "List created successfully.")
            return redirect("list:detail", list_slug=list_obj.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("list:summary")
    else:
        form = ListForm()
    return render(request, "list/list_form.html", {"form": form})


@login_required
def list_detail(request: HttpRequest, list_slug: str):
    """
    Displays the details of a specific list, including its entries.
    """
    try:
        list_obj = List.objects.get(slug=list_slug, is_deleted=False)
        entries = ListEntry.objects.filter(list=list_obj).select_related("created_by").order_by("created_at")

        return render(
            request,
            "list/list_detail.html",
            {
                "list": list_obj,
                "entries": entries,
                "entry_form": ListEntryForm(),
                "completed_count": entries.filter(is_completed=True).count(),
                "pending_count": entries.filter(is_completed=False).count(),
            },
        )
    except List.DoesNotExist:
        messages.error(request, "List not found.")
        return redirect("list:summary")


@login_required
def list_edit(request: HttpRequest, list_slug: str):
    """
    Edits a list.
    """
    try:
        list_obj = List.objects.get(slug=list_slug, is_deleted=False)
    except List.DoesNotExist:
        messages.error(request, "List not found.")
        return redirect("list:summary")

    if request.method == "POST":
        form = ListForm(request.POST, instance=list_obj)
        if form.is_valid():
            list_obj = form.save()
            messages.success(request, "List updated successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return redirect("list:detail", list_slug=list_obj.slug)
    else:
        form = ListForm(instance=list_obj)
        return render(request, "list/list_form.html", {"form": form, "list": list_obj})


@login_required
def list_delete(request: HttpRequest, list_slug: str):
    """
    Deletes a list and all associated entries.
    """
    list_obj = get_object_or_404(List, slug=list_slug, is_deleted=False)
    if request.method == "POST":
        list_obj.is_deleted = True
        list_obj.updated_by = request.user
        list_obj.save()
        messages.success(request, "List deleted successfully.")
        return redirect("list:summary")

    return render(request, "list/list_confirm_delete.html", {"list": list_obj})


@login_required
def list_entry_create(request: HttpRequest, list_slug: str):
    """
    Create a new list entry.
    """
    try:
        list_obj = List.objects.get(slug=list_slug, is_deleted=False)
    except List.DoesNotExist:
        messages.error(request, "List not found.")
        return redirect("list:summary")

    if request.method == "POST":
        form = ListEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.list = list_obj
            entry.created_by = request.user
            entry.save()
            messages.success(request, "List entry created successfully.")
            return redirect("list:detail", list_slug=list_slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("list:detail", list_slug=list_slug)
    else:
        return render(request, "list/list_entry_create.html", {"form": ListEntryForm(), "list": list_obj})


@login_required
def list_entry_detail(request: HttpRequest, entry_slug: str):
    """
    Displays the details of a specific list entry.
    """
    try:
        entry = ListEntry.objects.select_related("list", "created_by", "updated_by").get(
            slug=entry_slug, is_deleted=False
        )
        return render(request, "list/list_entry_detail.html", {"entry": entry})
    except ListEntry.DoesNotExist:
        messages.error(request, "List entry not found.")
        return redirect("list:summary")


@login_required
def list_entry_edit(request: HttpRequest, entry_slug: str):
    """
    Edit a list entry.
    """
    try:
        entry = ListEntry.objects.get(slug=entry_slug, is_deleted=False)
    except ListEntry.DoesNotExist:
        messages.error(request, "List entry not found.")
        return redirect("list:summary")

    if request.method == "POST":
        form = ListEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.updated_by = request.user
            entry.save()
            messages.success(request, "List entry updated successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return redirect("list:detail", list_slug=entry.list.slug)
    else:
        form = ListEntryForm(instance=entry)
        return render(request, "list/list_entry_form.html", {"form": form, "entry": entry})


@login_required
def list_entry_delete(request: HttpRequest, entry_slug: str):
    """
    Delete a list entry.
    """
    try:
        entry = ListEntry.objects.get(slug=entry_slug)
        list_slug = entry.list.slug
        entry.delete()
        messages.success(request, "List entry deleted successfully.")
    except ListEntry.DoesNotExist:
        messages.error(request, "List entry not found.")
        return redirect("list:summary")

    return redirect("list:detail", list_slug=list_slug)


@login_required
def template_download(request: HttpRequest):
    """
    Generates and returns an Excel file template for list import.
    """
    df = pl.DataFrame(
        data={
            "list_name": [
                "Grocery Shopping",
                "Grocery Shopping",
                "Grocery Shopping",
                "Party Supplies",
                "Party Supplies",
                "Party Supplies",
                "Hardware Store",
                "Hardware Store",
            ],
            "item": ["Milk", "Bread", "Apples", "Balloons", "Paper Plates", "Plastic Cups", "Screws", "Paint Brush"],
            "description": [
                "Whole milk, 1 gallon",
                "Whole wheat bread loaf",
                "Organic red apples",
                "Colorful party balloons pack",
                "White disposable paper plates",
                "Clear plastic cups for drinks",
                "Phillips head screws 1 inch",
                "Medium size paint brush for walls",
            ],
            "vendor": [
                "Costco",
                "Costco",
                "Amazon",
                "Party City",
                "Party City",
                "Party City",
                "Home Depot",
                "Home Depot",
            ],
            "quantity": [2, 1, 3, 1, 2, 4, 1, 2],
            "unit_price": [3.49, 2.99, 1.99, 4.99, 3.49, 2.99, 5.99, 7.49],
            "additional_price": [2.00, 1.00, 0.99, 13.99, 12.99, 10.99, 0.50, 1.50],
            "url": [
                "https://www.costco.com/milk",
                "https://www.costco.com/bread",
                "https://www.amazon.com/apples",
                "https://www.partycity.com/balloons",
                "https://www.partycity.com/paper-plates",
                "https://www.partycity.com/plastic-cups",
                "https://www.homedepot.com/s/screws",
                "https://www.homedepot.com/s/paint%20brush",
            ],
            "expense": [
                "Breakfast",
                "Lunch",
                "Lunch",
                "Party",
                "Party",
                "Party",
                "Home Improvement",
                "Home Improvement",
            ],
            "is_completed": ["FALSE", "TRUE", "FALSE", "FALSE", "TRUE", "FALSE", "FALSE", "FALSE"],
        }
    )
    output = io.BytesIO()
    df.write_excel(output)
    output.seek(0)

    # Create the HTTP response with the Excel file
    response = HttpResponse(
        output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="list_import_template.xlsx"'

    return response


@login_required
def list_import(request: HttpRequest):
    """
    Handles the import of lists from an Excel file.
    """
    if request.method == "POST" and request.user.is_authenticated and isinstance(request.user, User):
        uploaded_file = request.FILES.get("excel_file")

        if not uploaded_file:
            messages.error(request, "Please select an Excel file to upload.")
            return redirect("list:summary")

        try:
            df = pl.read_excel(io.BytesIO(uploaded_file.read()))

            # Validate required columns
            required_columns = ["list_name", "item"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                messages.error(request, f"Missing required columns: {', '.join(missing_columns)}")
                return redirect("list:summary")

            # Process the data
            success_count = 0
            updated_count = 0
            error_count = 0
            errors = []

            for index, row in enumerate(df.to_dicts()):
                try:
                    # Get or create list
                    list_name = str(row.get("list_name", "")).strip()
                    if not list_name or list_name == "null":
                        errors.append(f"Row {index + 2}: List name is required")
                        error_count += 1
                        continue

                    list_obj, created = List.objects.get_or_create(
                        name=list_name,
                        defaults={
                            "slug": slugify(list_name),
                            "created_by": request.user,
                        },
                    )

                    # Validate item name
                    item = str(row.get("item", "")).strip()
                    if not item or item == "null":
                        errors.append(f"Row {index + 2}: Item name is required")
                        error_count += 1
                        continue

                    # Process optional fields
                    description = str(row.get("description", "")).strip() if row.get("description") is not None else ""
                    if description == "null":
                        description = ""

                    # Parse completed status
                    is_completed = False
                    if row.get("is_completed") is not None:
                        completed_val = str(row["is_completed"]).lower().strip()
                        is_completed = completed_val in ["true", "1", "yes", "completed", "done"]
                        logger.info(f"Row {index + 2}: Parsed is_completed as {is_completed}")

                    # Parse quantity
                    quantity = 1
                    if row.get("quantity") is not None:
                        try:
                            quantity = int(float(row["quantity"]))
                            if quantity <= 0:
                                quantity = 1
                        except (ValueError, TypeError):
                            quantity = 1

                    # Parse unit price
                    unit_price = 0.00
                    if row.get("unit_price") is not None:
                        try:
                            unit_price = float(row["unit_price"])
                            if unit_price < 0:
                                unit_price = 0.00
                        except (ValueError, TypeError):
                            unit_price = 0.00

                    # Parse additional price
                    additional_price = 0.00
                    if row.get("additional_price") is not None:
                        try:
                            additional_price = float(row["additional_price"])
                            if additional_price < 0:
                                additional_price = 0.00
                        except (ValueError, TypeError):
                            additional_price = 0.00

                    # Prepare defaults for get_or_create
                    defaults = {
                        "description": description,
                        "created_by": request.user,
                        "is_completed": is_completed,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "additional_price": additional_price,
                    }

                    # Set completed_at if item is completed
                    if is_completed:
                        defaults["completed_at"] = timezone.now()

                    # Create/update list entry
                    logger.info(f"Row {index + 2}: Creating/updating list entry for {item}")
                    list_entry, created = ListEntry.objects.get_or_create(
                        item=item,
                        list=list_obj,
                        defaults=defaults,
                    )
                    logger.info(f"Row {index + 2}: List entry {'created' if created else 'found'}")

                    # If item already existed, update it with new values
                    if not created:
                        list_entry.description = description
                        list_entry.is_completed = is_completed
                        list_entry.quantity = quantity
                        list_entry.unit_price = unit_price
                        list_entry.additional_price = additional_price
                        list_entry.updated_by = request.user

                        # Handle completed_at field
                        if is_completed and not list_entry.completed_at:
                            list_entry.completed_at = timezone.now()
                        elif not is_completed:
                            list_entry.completed_at = None

                        list_entry.save()
                        updated_count += 1
                    else:
                        success_count += 1

                    # add vendor if supplied
                    if row.get("vendor") is not None:
                        vendor_name = str(row["vendor"]).strip()
                        if vendor_name and vendor_name.lower() != "null":
                            vendor, _ = Contact.objects.get_or_create(
                                company=vendor_name,
                                defaults={"created_by": request.user},
                            )
                            list_entry.vendor = vendor
                            list_entry.save()

                    # add expense if supplied
                    if row.get("expense") is not None:
                        expense = str(row["expense"]).strip()
                        if expense and expense.lower() != "null":
                            uncategorized_category, _ = Category.objects.get_or_create(
                                name="Uncategorized",
                                defaults={"created_by": request.user, "slug": slugify("Uncategorized")},
                            )
                            expense_item, _ = Expense.objects.get_or_create(
                                item=expense,
                                defaults={"created_by": request.user, "category": uncategorized_category},
                            )
                            list_entry.associated_expense = expense_item
                            list_entry.save()

                    # add URL if supplied
                    if row.get("url") is not None:
                        url = str(row["url"]).strip()
                        if url and url.lower() != "null":
                            list_entry.url = url
                            list_entry.save()

                except Exception as e:
                    logger.error(f"Error processing row {index + 2}: {str(e)}")
                    errors.append(f"Row {index + 2}: {str(e)}")
                    error_count += 1

            # Show results
            if success_count > 0:
                messages.success(request, f"Successfully imported {success_count} new list items.")

            if updated_count > 0:
                messages.info(request, f"Updated {updated_count} existing list items.")

            if error_count > 0:
                messages.warning(request, f"{error_count} items had errors and were skipped.")
                for error in errors[:5]:  # Show first 5 errors
                    messages.error(request, error)

            if not success_count and not updated_count and not error_count:
                messages.info(request, "No list items found in the uploaded file.")

        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
            return redirect("list:summary")
    else:
        messages.error(request, "Invalid form submission.")
        return redirect("list:summary")

    return redirect("list:summary")


# Alias for backwards compatibility
summary = list_summary
create = list_create
