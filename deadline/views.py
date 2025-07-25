from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import polars as pl
import io
from django.http import HttpResponse
from django.contrib import messages
from deadline.forms import DeadlineForm, DeadlineImportForm, DeadlineListForm
from deadline.models import Deadline, DeadlineList
from datetime import datetime
from django.db.models import Count, Q
from users.models import User
import logging

logger = logging.getLogger(__name__)


@login_required
def deadline_summary(request: HttpRequest) -> HttpResponse:
    """ """
    deadline_lists = (
        DeadlineList.objects.filter(is_deleted=False)
        .prefetch_related("deadline_set")
        .annotate(
            total_deadline=Count("deadline"),
            completed_deadline=Count("deadline", filter=Q(deadline__completed=True)),
            pending_deadline=Count("deadline", filter=Q(deadline__completed=False)),
        )
        .order_by("name")
    )

    context = {
        "deadline_lists": deadline_lists,
        "form": DeadlineImportForm(),
        "completed_deadline": sum(list.completed_count for list in deadline_lists),
        "pending_deadline": sum(list.pending_count for list in deadline_lists),
    }
    return render(request, "deadline/deadline_summary.html", context)


@login_required
def deadline_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DeadlineForm(request.POST, user=request.user)
        if form.is_valid():
            deadline = form.save(commit=False)
            deadline.created_by = request.user
            deadline.updated_by = request.user
            deadline.save()
            messages.success(request, "Deadline created successfully.")
            return redirect("deadline:deadline_list_detail", deadline_list_slug=deadline.deadline_list.slug)
        else:
            messages.error(request, "Please correct the errors below.")
            return render(
                request, "deadline/deadline_form.html", {"form": DeadlineForm(user=request.user, object=form.instance)}
            )
    else:
        context = {
            "form": DeadlineForm(),
        }

        return render(request, "deadline/deadline_form.html", context)


@login_required
def deadline_edit(request: HttpRequest, deadline_slug: str) -> HttpResponse:
    try:
        deadline = Deadline.objects.get(slug=deadline_slug, is_deleted=False)
    except Deadline.DoesNotExist:
        messages.error(request, "Deadline not found.")
        return redirect("deadline:deadline_summary")

    if request.method == "POST" and deadline:
        form = DeadlineForm(request.POST, instance=deadline)
        if form.is_valid():
            form.save()
            messages.success(request, "Deadline updated successfully.")
            return redirect("deadline:deadline_list_detail", deadline_list_slug=deadline.deadline_list.slug)
    else:
        form = DeadlineForm(instance=deadline)

    context = {
        "form": form,
        "deadline": deadline,
    }
    return render(request, "deadline/deadline_form.html", context)


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
        return redirect("deadline:deadline_list_detail", deadline_list_slug=deadline.deadline_list.slug)
    else:
        messages.error(request, "Invalid request method.")
        return redirect("deadline:deadline_summary")


@login_required
def deadline_toggle_complete(request: HttpRequest, deadline_slug: str) -> HttpResponse:
    """
    Toggle the completion status of a deadline.
    """
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("deadline:deadline_summary")
    try:
        deadline = Deadline.objects.get(slug=deadline_slug, is_deleted=False)
    except Deadline.DoesNotExist:
        messages.error(request, "Deadline not found.")
        return redirect("deadline:deadline_summary")

    deadline.completed = not deadline.completed
    deadline.save()
    status = "completed" if deadline.completed else "pending"
    messages.success(request, f"Deadline marked as {status}.")
    return redirect("deadline:deadline_list_detail", deadline_list_slug=deadline.deadline_list.slug)


@login_required
def deadline_list_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DeadlineForm(request.POST, user=request.user)
        if form.is_valid():
            deadline_list = form.save(commit=False)
            deadline_list.created_by = request.user
            deadline_list.updated_by = request.user
            deadline_list.save()
            messages.success(request, "Deadline list created successfully.")
            return redirect("deadline:deadline_list_detail", deadline_list_slug=deadline_list.slug)
        else:
            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                "deadline/deadline_list_form.html",
                {"form": DeadlineForm(user=request.user, object=form.instance)},
            )
    else:
        context = {
            "form": DeadlineForm(),
        }
        return render(request, "deadline/deadline_list_form.html", context)


@login_required
def deadline_list_detail(request: HttpRequest, deadline_list_slug: str) -> HttpResponse:
    """
    View to display details of a specific deadline list.
    """
    try:
        deadline_list = DeadlineList.objects.get(slug=deadline_list_slug, is_deleted=False)

    except DeadlineList.DoesNotExist:
        messages.error(request, "Deadline list not found.")
        return redirect("deadline:deadline_summary")

    context = {
        "deadline_list": deadline_list,
        "deadlines": deadline_list.deadline_set.filter(is_deleted=False).order_by("due_date"),
    }
    return render(request, "deadline/deadline_list_detail.html", context)


@login_required
def deadline_list_delete(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DeadlineForm(request.POST)
        if form.is_valid():
            deadline_list = form.save(commit=False)
            deadline_list.is_deleted = True
            deadline_list.updated_by = request.user
            deadline_list.save()
            messages.success(request, "Deadline list deleted successfully.")
            return redirect("deadline:deadline_summary")
        else:
            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                "deadline/deadline_list_form.html",
                {"form": DeadlineForm(user=request.user, object=form.instance)},
            )
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
        form = DeadlineListForm(request.POST)
        if form.is_valid():
            deadline_list = form.save(commit=False)
            deadline_list.created_by = request.user
            deadline_list.updated_by = request.user
            deadline_list.save()
            messages.success(request, "Deadline list updated successfully.")
            return redirect("deadline:deadline_list_detail", deadline_list_slug=deadline_list.slug)
        else:
            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                "deadline/deadline_list_form.html",
                {"form": DeadlineListForm(object=form.instance)},
            )
    else:
        context = {
            "form": DeadlineListForm(instance=deadline_list),
            "deadline_list": deadline_list,
        }
        return render(request, "deadline/deadline_list_form.html", context)


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
                                except:
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
