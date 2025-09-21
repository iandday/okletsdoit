from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import polars as pl
import io
from django.http import HttpResponse
from django.contrib import messages
from shared_helpers.table_helpers import format_row_action_cell
from deadline.forms import DeadlineForm, DeadlineImportForm, DeadlineListForm
from deadline.models import Deadline, DeadlineList
from datetime import datetime
from django.db.models import Count, Q
from users.models import User
import logging

logger = logging.getLogger("__name__")

logger.error("Deadline views loaded")


@login_required
def deadline_summary(request: HttpRequest) -> HttpResponse:
    """
    Display a summary of all deadline lists and their progress.
    """
    deadline_lists = DeadlineList.objects.filter(is_deleted=False).order_by("name")

    context = {
        "deadline_lists": deadline_lists,
        "form": DeadlineImportForm(),
        "delete_modal_url": reverse("deadline:deadline_list_delete_modal"),
        "block_title": "Deadline Summary",
    }
    return render(request, "deadline/deadline_summary.html", context)


@login_required
def deadline_detail(request: HttpRequest, deadline_slug: str) -> HttpResponse:
    """Display details for a single deadline."""
    try:
        deadline = Deadline.objects.select_related("deadline_list", "assigned_to").get(
            slug=deadline_slug, is_deleted=False
        )
    except Deadline.DoesNotExist:
        messages.error(request, "Deadline not found.")
        return redirect("deadline:deadline_summary")

    breadcrumbs = [
        {"title": "Deadline Summary", "url": reverse("deadline:deadline_summary")},
        {
            "title": deadline.deadline_list.name,
            "url": reverse("deadline:deadline_list_detail", args=[deadline.deadline_list.slug]),
        },
        {"title": f"{deadline}", "url": None},
    ]

    context = {
        "block_title": f"{deadline}",
        "breadcrumbs": breadcrumbs,
        "title": f"{deadline}",
        "object": deadline,
        "edit_url": reverse("deadline:deadline_edit", args=[deadline.slug]),
        "status": deadline.completed,
        "status_text": "Complete" if deadline.completed else "Pending",
        "link_url": None,
        "image_url": None,
        "delete_modal_url": reverse("deadline:deadline_delete_modal"),
    }

    return render(request, "deadline/deadline_detail.html", context)


@login_required
def deadline_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DeadlineForm(request.POST, user=request.user)
        if form.is_valid():
            deadline: Deadline = form.save(commit=False)
            deadline.created_by = request.user
            deadline.updated_by = request.user
            deadline.save()
            messages.success(request, "Deadline created successfully.")
            return redirect(reverse("deadline:deadline_detail", args=[deadline.slug]))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # check for deadline_list value in request.GET
        deadline_list_slug = request.GET.get("list")
        if deadline_list_slug:
            try:
                deadline_list = DeadlineList.objects.get(slug=deadline_list_slug, is_deleted=False)
                form = DeadlineForm(initial={"deadline_list": deadline_list})
            except DeadlineList.DoesNotExist:
                messages.error(request, "Deadline list not found.")
                return redirect("deadline:deadline_summary")
        else:
            form = DeadlineForm()

    intro = "Create Deadline"
    breadcrumbs = [
        {"title": "Deadline List", "url": reverse("deadline:deadline_summary")},
        {"title": "Create Deadline", "url": None},
    ]
    cancel_url = reverse("deadline:deadline_summary")

    context = {
        "block_title": "Create Deadline",
        "breadcrumbs": breadcrumbs,
        "title": "Create Deadline",
        "intro": intro,
        "form": form,
        "submit_text": "Create",
        "cancel_url": cancel_url,
        "first_field": "item",
    }
    return render(request, "form/object.html", context)


@login_required
def deadline_edit(request: HttpRequest, deadline_slug: str) -> HttpResponse:
    try:
        deadline = Deadline.objects.get(slug=deadline_slug, is_deleted=False)
    except Deadline.DoesNotExist:
        messages.error(request, "Deadline not found.")
        return redirect("deadline:deadline_summary")

    if request.method == "POST":
        form = DeadlineForm(request.POST, instance=deadline)
        if form.is_valid():
            # set the updated_by field and save
            deadline: Deadline = form.save(commit=False)
            deadline.updated_by = request.user
            deadline.save()
            messages.success(request, "Deadline updated successfully.")
            return redirect("deadline:deadline_detail", deadline_slug=deadline.slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DeadlineForm(instance=deadline)

    # configure rest of template context
    intro = f"Edit Deadline: {deadline}"
    breadcrumbs = [
        {"title": "Deadline List", "url": reverse("deadline:deadline_summary")},
        {
            "title": deadline.deadline_list,
            "url": reverse("deadline:deadline_list_detail", args=[deadline.deadline_list.slug]),
        },
        {"title": deadline, "url": None},
    ]
    cancel_url = reverse("deadline:deadline_detail", args=[deadline.slug])

    context = {
        "block_title": "Edit Deadline",
        "breadcrumbs": breadcrumbs,
        "title": f"Edit Deadline: {deadline}",
        "intro": intro,
        "form": form,
        "object": deadline,
        "submit_text": "Save Changes",
        "cancel_url": cancel_url,
        "first_field": "item",
    }
    return render(request, "form/object.html", context)


@login_required
def deadline_delete_modal(request: HttpRequest) -> HttpResponse:
    """
    Render the modal content for deleting a deadline.
    """
    deadline_slug = request.GET.get("slug")
    if not deadline_slug:
        return JsonResponse({"error": "Deadline slug is required"}, status=400)
    try:
        deadline = Deadline.objects.get(slug=deadline_slug, is_deleted=False)
    except Deadline.DoesNotExist:
        return JsonResponse({"error": "Deadline not found"}, status=404)

    context = {
        "object": deadline,
        "object_type": "Deadline",
        "action_url": reverse("deadline:deadline_delete", args=[deadline.slug]),
    }
    return render(request, "components/modal/object_delete_modal_body.html", context)


@login_required
def deadline_delete(request: HttpRequest, deadline_slug: str) -> HttpResponse:
    if request.method == "POST":
        try:
            deadline = Deadline.objects.get(slug=deadline_slug, is_deleted=False)
        except Deadline.DoesNotExist:
            messages.error(request, "Deadline not found.")
            return redirect("deadline:deadline_summary")
        deadline.is_deleted = True
        deadline.save()
        messages.success(request, "Deadline deleted successfully.")
        return redirect(f"{reverse('deadline:list')}?list={deadline.deadline_list.slug}")
    else:
        messages.error(request, "Invalid request method.")
        return redirect("deadline:deadline_summary")


@login_required
def deadline_toggle_complete(request: HttpRequest, deadline_slug: str) -> HttpResponse:
    """
    Toggle the completion status of a deadline.
    """

    try:
        deadline = Deadline.objects.get(slug=deadline_slug, is_deleted=False)
    except Deadline.DoesNotExist:
        messages.error(request, "Deadline not found.")
        return redirect("deadline:deadline_summary")

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
    else:
        deadline.completed = not deadline.completed
        deadline.save()
        status = "completed" if deadline.completed else "pending"
        messages.success(request, f"Deadline marked as {status}.")
    return redirect("deadline:deadline_detail", deadline_slug=deadline.slug)


@login_required
def deadline_data(request) -> JsonResponse:
    """JSON endpoint for DataTables"""

    list_slug = request.GET.get("list")

    # Get DataTables parameters
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")

    # Handle sorting
    order_column_index = request.GET.get("order[0][column]")
    order_direction = request.GET.get("order[0][dir]")
    order_column_name = request.GET.get(f"columns[{order_column_index}][name]")

    if list_slug:
        queryset = Deadline.objects.filter(deadline_list__slug=list_slug, is_deleted=False).select_related(
            "deadline_list"
        )
    else:
        queryset = Deadline.objects.filter(is_deleted=False).select_related("deadline_list")

    records_total = queryset.count()

    # Apply search filter if provided
    if search_value:
        queryset = queryset.filter(
            Q(name__icontains=search_value)
            | Q(description__icontains=search_value)
            | Q(assigned_to__first_name__icontains=search_value)
        )
    records_filtered = queryset.count()

    # sort the queryset if order_column_name is provided
    if order_column_name:
        if order_direction == "desc":
            order_by = f"-{order_column_name}"
        else:
            order_by = order_column_name
        queryset = queryset.order_by(order_by)

    # Apply pagination
    queryset = queryset[start : start + length]

    # Prepare data for DataTables
    data = []
    for deadline in queryset:
        menu_content = format_row_action_cell(
            detail_url=reverse("deadline:deadline_detail", args=[deadline.slug]),
            update_url=reverse("deadline:deadline_edit", args=[deadline.slug]),
            slug=deadline.slug,
        )
        if deadline.deadline_list:
            deadline_list_url = f'<a href="{reverse("deadline:deadline_list_detail", args=[deadline.deadline_list.slug])}">{deadline.deadline_list.name}</a>'
        else:
            deadline_list_url = "-"
        data.append(
            {
                "name": f'<a href="{reverse("deadline:deadline_detail", args=[deadline.slug])}">{deadline.name}</a>',
                "description": deadline.description or "-",
                "list": deadline_list_url if deadline.deadline_list else "-",
                "due_date": deadline.due_date.strftime("%Y-%m-%d") if deadline.due_date else None,
                "assigned_to": deadline.assigned_to.first_name if deadline.assigned_to else "Unassigned",
                "status": "Completed" if deadline.completed else "Pending",
                "menu_content": menu_content,
            }
        )

    return JsonResponse(
        {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        }
    )


@login_required
def list(request: HttpRequest):
    # check if list is in parameters
    list_slug = request.GET.get("list")
    context = {"delete_modal_url": reverse("deadline:deadline_delete_modal"), "form": DeadlineForm()}

    if list_slug:
        deadline_list = DeadlineList.objects.get(slug=list_slug, is_deleted=False)
        if not deadline_list:
            return redirect("deadline:list")
        context["list"] = deadline_list  # type: ignore[assignment]

    return render(request, "deadline/deadline_all.html", context)


@login_required
def deadline_list_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DeadlineListForm(request.POST)
        if form.is_valid():
            deadline_list: DeadlineList = form.save(commit=False)
            deadline_list.created_by = request.user
            deadline_list.updated_by = request.user
            deadline_list.save()
            messages.success(request, "Deadline list created successfully.")
            return redirect("deadline:deadline_list_detail", deadline_list_slug=deadline_list.slug)
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = DeadlineListForm()
    # configure rest of template context
    intro = "Create Deadline List"
    breadcrumbs = [
        {"title": "Deadlines", "url": reverse("deadline:deadline_summary")},
        {"title": "Create Deadline List", "url": None},
    ]
    cancel_url = reverse("deadline:deadline_summary")

    context = {
        "block_title": "Create Deadline List",
        "breadcrumbs": breadcrumbs,
        "title": "Create Deadline List",
        "intro": intro,
        "form": form,
        "submit_text": "Create",
        "cancel_url": cancel_url,
        "first_field": "name",
    }
    return render(request, "form/object.html", context)


@login_required
def deadline_list_detail(request: HttpRequest, deadline_list_slug: str) -> HttpResponse:
    try:
        obj = DeadlineList.objects.get(slug=deadline_list_slug, is_deleted=False)
    except DeadlineList.DoesNotExist:
        messages.error(request, "Deadline list not found.")
        return redirect("deadline:deadline_summary")

    breadcrumbs = [
        {"title": "Deadline Summary", "url": reverse("deadline:deadline_summary")},
        {"title": obj, "url": None},
    ]

    context = {
        "block_title": f"{obj}",
        "breadcrumbs": breadcrumbs,
        "title": f"{obj}",
        "object": obj,
        "edit_url": reverse("deadline:deadline_list_edit", args=[obj.slug]),
        "status": obj.completion_percentage > 0,
        "status_text": f"{obj.completion_percentage}% Complete" if obj.completion_percentage > 0 else "Not Started",
        "link_url": None,
        "image_url": None,
        "add_object_url": f"{reverse('deadline:deadline_create')}?list={obj.slug}",
        "delete_modal_url": reverse("deadline:deadline_list_delete_modal"),
        "completed_count": obj.completed_count,
        "pending_count": obj.pending_count,
        "entries": obj.deadlines.all(),
    }
    return render(request, "deadline/deadline_list_detail.html", context)


@login_required
def deadline_list_delete_modal(request: HttpRequest) -> HttpResponse | JsonResponse:
    """
    Render the modal content for deleting a deadline.
    """

    deadline_list_slug = request.GET.get("slug")
    if not deadline_list_slug:
        return JsonResponse({"error": "Deadline list slug is required"}, status=400)
    try:
        deadline_list = DeadlineList.objects.get(slug=deadline_list_slug, is_deleted=False)
    except DeadlineList.DoesNotExist:
        return JsonResponse({"error": "Deadline list not found"}, status=404)

    deadline_list = DeadlineList.objects.get(slug=deadline_list_slug, is_deleted=False)

    context = {
        "object": deadline_list,
        "object_type": "Deadline List",
        "action_url": reverse("deadline:deadline_list_delete", args=[deadline_list.slug]),
    }

    return render(request, "components/modal/object_delete_modal_body.html", context)


@login_required
def deadline_list_delete(request: HttpRequest, deadline_list_slug: str) -> HttpResponse:
    if request.method == "POST":
        try:
            deadline_list = DeadlineList.objects.get(slug=deadline_list_slug, is_deleted=False)
        except DeadlineList.DoesNotExist:
            messages.error(request, "Deadline list not found.")
            return redirect("deadline:deadline_summary")
        deadline_list.is_deleted = True
        deadline_list.save()

        messages.success(request, "Deadline list deleted successfully.")
        return redirect("deadline:deadline_summary")

    else:
        messages.error(request, "Invalid request method.")
        return redirect("deadline:deadline_summary")


@login_required
def deadline_list_edit(request: HttpRequest, deadline_list_slug: str) -> HttpResponse:
    try:
        deadline_list = DeadlineList.objects.get(slug=deadline_list_slug, is_deleted=False)
    except DeadlineList.DoesNotExist:
        messages.error(request, "Deadline list not found.")
        return redirect("deadline:deadline_summary")

    if request.method == "POST":
        form = DeadlineListForm(request.POST, instance=deadline_list)
        if form.is_valid():
            deadline_list: DeadlineList = form.save(commit=False)
            deadline_list.updated_by = request.user
            deadline_list.save()
            messages.success(request, "Deadline list updated successfully.")
            return redirect("deadline:deadline_list_detail", deadline_list_slug=deadline_list.slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DeadlineListForm(instance=deadline_list)

    # configure rest of template context
    intro = f"Edit Deadline List: {deadline_list}"
    breadcrumbs = [
        {"title": "Deadlines", "url": reverse("deadline:deadline_summary")},
        {
            "title": deadline_list,
            "url": reverse("deadline:deadline_list_detail", args=[deadline_list.slug]),
        },
        {"title": "Edit", "url": None},
    ]
    cancel_url = reverse("deadline:deadline_list_detail", args=[deadline_list.slug])

    context = {
        "block_title": "Edit Deadline List",
        "breadcrumbs": breadcrumbs,
        "title": f"Edit Deadline List: {deadline_list}",
        "intro": intro,
        "form": form,
        "object": deadline_list,
        "submit_text": "Save Changes",
        "cancel_url": cancel_url,
        "first_field": "name",
    }
    return render(request, "form/object.html", context)


@login_required
def deadline_import(request: HttpRequest) -> HttpResponse:
    """
    Handles the import of deadlines from an uploaded Excel file and provides a template for import.
    - On POST:
        - Validates the uploaded form and Excel file.
        - Reads the Excel file using Polars and checks for required columns.
        - Iterates through each row to create or update Deadline and DeadlineList objects.
        - Validates and parses fields such as deadline list name, deadline name, description, due date, priority, assigned user, and completion status.
        - Tracks and reports the number of successful imports, updates, and errors.
        - Displays appropriate success, info, warning, and error messages to the user.
        - Redirects to the deadline summary page after processing.
    - On GET:
        - Generates and returns an Excel template for deadline import with sample data.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Redirects to summary page or returns an Excel file template for import.
    """

    # Implementation for handling file upload and processing goes here
    if request.method == "POST":
        form = DeadlineImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get("excel_file")
            if uploaded_file:
                try:
                    df = pl.read_excel(io.BytesIO(uploaded_file.read()))

                    # Validate required columns
                    required_columns = ["deadline_list_name", "name"]
                    missing_columns = [col for col in required_columns if col not in df.columns]

                    if missing_columns:
                        messages.error(request, f"Missing required columns: {', '.join(missing_columns)}")
                        return redirect("deadline:deadline_summary")

                    # Process the data
                    success_count = 0
                    error_count = 0
                    update_count = 0
                    errors = []

                    # Get all users for assignment lookup
                    users_dict = {user.email.lower(): user for user in User.objects.all()}
                    users_dict.update({user.email.lower(): user for user in User.objects.all()})

                    # Convert to Python dicts for iteration
                    for index, row in enumerate(df.to_dicts()):
                        try:
                            # Get or create deadline list
                            deadline_list_name = str(row.get("deadline_list_name", "")).strip()
                            if not deadline_list_name or deadline_list_name == "null":
                                errors.append(f"Row {index + 2}: Deadline list name is required")
                                error_count += 1
                                continue

                            deadline_list, created = DeadlineList.objects.get_or_create(
                                name=deadline_list_name,
                                defaults={
                                    "created_by": request.user,
                                    "updated_by": request.user,
                                },
                            )

                            # Validate deadline name
                            name = str(row.get("name", "")).strip()
                            if not name or name == "null":
                                errors.append(f"Row {index + 2}: Deadline name is required")
                                error_count += 1
                                continue

                            description = (
                                str(row.get("description", "")).strip() if row.get("description", None) else None
                            )

                            # Parse due date
                            due_date = None
                            if row.get("due_date") is not None:
                                try:
                                    due_date_val = row["due_date"]
                                    if isinstance(due_date_val, str):
                                        due_date = datetime.strptime(due_date_val, "%Y-%m-%d").date()
                                    else:
                                        # Handle datetime objects from Excel
                                        due_date = (
                                            due_date_val.date() if hasattr(due_date_val, "date") else due_date_val
                                        )
                                except Exception:
                                    errors.append(f"Row {index + 2}: Invalid due date format")
                                    error_count += 1
                                    continue

                            # Parse assigned user
                            assigned_to = None
                            if row.get("assigned_to") is not None:
                                assigned_email = str(row["assigned_to"]).strip().lower()
                                if assigned_email and assigned_email != "null":
                                    assigned_to = users_dict.get(assigned_email)
                                    if not assigned_to:
                                        errors.append(f"Row {index + 2}: User '{assigned_email}' not found")
                                        error_count += 1
                                        continue

                            # Parse completed status
                            completed = False
                            if row.get("completed") is not None:
                                completed_val = str(row["completed"]).lower().strip()
                                completed = completed_val in ["true", "1", "yes", "completed", "done"]

                            deadline, created = Deadline.objects.get_or_create(
                                name=name,
                                deadline_list=deadline_list,
                                is_deleted=False,
                                defaults={
                                    "created_by": request.user,
                                    "updated_by": request.user,
                                    "description": description,
                                    "due_date": due_date,
                                    "assigned_to": assigned_to,
                                    "completed": completed,
                                },
                            )

                            if created:
                                success_count += 1
                            else:
                                # Update existing deadline
                                deadline.description = description
                                deadline.due_date = due_date
                                deadline.assigned_to = assigned_to
                                deadline.completed = completed
                                deadline.updated_by = request.user
                                deadline.save()
                                update_count += 1

                        except Exception as e:
                            errors.append(f"Row {index + 2}: {str(e)}")
                            error_count += 1

                    # Show results
                    if success_count > 0:
                        messages.success(request, f"Successfully imported {success_count} deadlines.")

                    if update_count > 0:
                        messages.info(request, f"Updated {update_count} existing deadlines.")

                    if error_count > 0:
                        messages.warning(request, f"{error_count} deadlines had errors and were skipped.")
                        for error in errors[:5]:  # Show first 5 errors
                            messages.error(request, error)

                    if not success_count and not update_count and not error_count:
                        messages.info(request, "No deadlines found in the uploaded file.")

                except Exception as e:
                    messages.error(request, f"Error processing file: {str(e)}")

            else:
                messages.error(request, "Please select an Excel file to upload.")
                return redirect("deadline:deadline_summary")
        else:
            messages.error(request, "Invalid form submission. Please try again.")
        return redirect("deadline:deadline_summary")

    df = pl.DataFrame(
        data={
            "deadline_list_name": ["Wedding Venue", "Wedding Venue", "Catering", "Photography"],
            "name": ["Book ceremony location", "Book reception venue", "Choose menu options", "Hire photographer"],
            "description": [
                "Find and book the perfect ceremony location",
                "Reserve reception venue for 100 guests",
                "Select appetizers and main courses",
                "Find professional wedding photographer",
            ],
            "due_date": ["2024-03-15", "2024-03-20", "2024-04-01", "2024-02-28"],
            "completed": ["FALSE", "FALSE", "FALSE", "TRUE"],
        }
    )
    output = io.BytesIO()
    df.write_excel(output)
    output.seek(0)

    # Create the HTTP response with the Excel file
    response = HttpResponse(
        output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="deadline_import_template.xlsx"'

    return response
