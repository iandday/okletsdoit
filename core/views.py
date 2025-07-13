import logging
import uuid
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib import messages
from django.http import HttpResponse
from django.utils.text import slugify
import polars as pl
import io
from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from urllib3 import request


from core.forms import IdeaForm, IdeaImportForm, TaskImportForm, TaskListForm, TaskForm
from core.models import Idea, TaskList, Task
from users.models import User

logger = logging.getLogger(__name__)


def home(request: HttpRequest):
    """
    Render the main page of the application.
    """
    return render(request, "core/index.html")


def venue(request: HttpRequest):
    """
    Render the venues page of the application.
    """
    return render(request, "core/venue.html")


def our_story(request: HttpRequest):
    """
    Render the 'Our Story' page of the application.
    """
    return render(request, "core/our_story.html")


def rsvp(request: HttpRequest):
    """
    Render the 'RSVP' page of the application.
    """
    return render(request, "core/rsvp.html")


def photos(request: HttpRequest):
    """
    Render the 'Photos' page of the application.
    """
    return render(request, "core/photos.html")


@login_required
def task_list(request: HttpRequest):
    """
    Render the 'Task List' page of the application.
    """

    if request.method == "POST":
        form = TaskImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get("excel_file")
            if uploaded_file:
                try:
                    df = pl.read_excel(io.BytesIO(uploaded_file.read()))

                    # Validate required columns
                    required_columns = ["task_list_name", "title"]
                    missing_columns = [col for col in required_columns if col not in df.columns]

                    if missing_columns:
                        messages.error(request, f"Missing required columns: {', '.join(missing_columns)}")
                        return redirect("task_list")

                    # Process the data
                    success_count = 0
                    error_count = 0
                    errors = []

                    # Get all users for assignment lookup
                    users_dict = {user.email.lower(): user for user in User.objects.all()}
                    users_dict.update({user.email.lower(): user for user in User.objects.all()})

                    # Convert to Python dicts for iteration
                    rows = df.to_dicts()

                    for index, row in enumerate(rows):
                        try:
                            # Get or create task list
                            task_list_name = str(row.get("task_list_name", "")).strip()
                            if not task_list_name or task_list_name == "null":
                                errors.append(f"Row {index + 2}: Task list name is required")
                                error_count += 1
                                continue

                            task_list, created = TaskList.objects.get_or_create(
                                name=task_list_name,
                                defaults={
                                    "slug": slugify(task_list_name),
                                    "created_by": request.user,
                                    "updated_by": request.user,
                                },
                            )

                            # Validate task title
                            title = str(row.get("title", "")).strip()
                            if not title or title == "null":
                                errors.append(f"Row {index + 2}: Task title is required")
                                error_count += 1
                                continue

                            # Check if task already exists
                            if Task.objects.filter(title=title, task_list=task_list, is_deleted=False).exists():
                                errors.append(
                                    f"Row {index + 2}: Task '{title}' already exists in list '{task_list_name}'"
                                )
                                error_count += 1
                                continue

                            # Process optional fields
                            description = (
                                str(row.get("description", "")).strip() if row.get("description") is not None else ""
                            )
                            if description == "null":
                                description = ""

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

                            # Parse priority
                            priority = None
                            if row.get("priority") is not None:
                                try:
                                    priority = int(row["priority"])
                                except:
                                    errors.append(f"Row {index + 2}: Priority must be a number")
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

                            # Create task
                            task = Task.objects.create(
                                title=title,
                                description=description,
                                slug=slugify(title),
                                task_list=task_list,
                                created_by=request.user,
                                updated_by=request.user,
                                due_date=due_date,
                                assigned_to=assigned_to,
                                completed=completed,
                                priority=priority,
                            )

                            success_count += 1

                        except Exception as e:
                            errors.append(f"Row {index + 2}: {str(e)}")
                            error_count += 1

                    # Show results
                    if success_count > 0:
                        messages.success(request, f"Successfully imported {success_count} tasks.")

                    if error_count > 0:
                        messages.warning(request, f"{error_count} tasks had errors and were skipped.")
                        for error in errors[:5]:  # Show first 5 errors
                            messages.error(request, error)

                    if not success_count and not error_count:
                        messages.info(request, "No tasks found in the uploaded file.")

                except Exception as e:
                    messages.error(request, f"Error processing file: {str(e)}")

            else:
                messages.error(request, "Please select an Excel file to upload.")
                task_lists = (
                    TaskList.objects.filter(is_deleted=False)
                    .prefetch_related("task_set")
                    .annotate(
                        total_tasks=Count("task"),
                        completed_tasks=Count("task", filter=Q(task__completed=True)),
                        pending_tasks=Count("task", filter=Q(task__completed=False)),
                    )
                    .order_by("name")
                )
                return render(request, "core/task_list.html", {"task_lists": task_lists})
        else:
            messages.error(request, "Invalid form submission. Please try again.")
            task_lists = (
                TaskList.objects.filter(is_deleted=False)
                .prefetch_related("task_set")
                .annotate(
                    total_tasks=Count("task"),
                    completed_tasks=Count("task", filter=Q(task__completed=True)),
                    pending_tasks=Count("task", filter=Q(task__completed=False)),
                )
                .order_by("name")
            )
            return render(request, "core/task_list.html", {"task_lists": task_lists})
        return redirect("task_list")

    task_lists = (
        TaskList.objects.filter(is_deleted=False)
        .prefetch_related("task_set")
        .annotate(
            total_tasks=Count("task"),
            completed_tasks=Count("task", filter=Q(task__completed=True)),
            pending_tasks=Count("task", filter=Q(task__completed=False)),
        )
        .order_by("name")
    )

    # Create task list forms for each task list
    task_list_forms = {}
    for task_list in task_lists:
        task_list_forms[task_list.id] = TaskListForm(instance=task_list)

    form = TaskImportForm()
    add_task_list_form = TaskListForm()
    return render(
        request,
        "core/task_list.html",
        {
            "task_lists": task_lists,
            "form": form,
            "task_list_forms": task_list_forms,
            "add_task_list_form": add_task_list_form,
        },
    )


@login_required
def task_list_create(request: HttpRequest):
    """
    Creates a new task list.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the task list page with a success message.
    """

    if request.method == "POST":
        form = TaskListForm(request.POST)
        if form.is_valid():
            task_list: TaskList = form.save(commit=False)
            task_list.created_by = request.user
            task_list.save()

            messages.success(request, "Task list created successfully.")
            return redirect("core:task_list_detail", task_list_slug=task_list.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("core:task_list")
    else:
        form = TaskListForm()
    return render(request, "core/task_list_form.html", {"form": form})


@login_required
def task_list_delete(request: HttpRequest, task_list_slug: str):
    """
    Deletes a task list and all associated tasks.

    Args:
        request (HttpRequest): The HTTP request object.
        task_list_slug (str): The slug of the task list to delete.

    Returns:
        HttpResponse: Redirects to the task list page with a success message.
    """
    task_list = get_object_or_404(TaskList, slug=task_list_slug, is_deleted=False)
    if request.method == "POST":
        task_list.is_deleted = True
        task_list.updated_by = request.user
        task_list.save()
        messages.success(request, "Task list deleted successfully.")
        return redirect("core:task_list")
    context = {"task_list": task_list}

    return render(request, "core/task_list_confirm_delete.html", context)


@login_required
def task_list_edit(request: HttpRequest, task_list_slug: str):
    """
    Edits a task list.

    Args:
        request (HttpRequest): The HTTP request object.
        task_list_slug (str): The slug of the task list to edit.

    Returns:
        HttpResponse: Redirects to the task list page with a success message.
    """
    try:
        task_list = TaskList.objects.get(slug=task_list_slug, is_deleted=False)
    except TaskList.DoesNotExist:
        messages.error(request, "Task list not found.")
        return redirect("core:task_list")

    if request.method == "POST":
        form = TaskListForm(request.POST, instance=task_list)

        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.updated_by = request.user
            task_list.save()
            messages.success(request, "Task list updated successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return redirect("core:task_list_detail", task_list_slug=task_list.slug)

    else:
        form = TaskListForm(instance=task_list)
        return render(request, "core/task_list_form.html", {"form": form, "task_list": task_list})
        messages.error(request, "Invalid request method.")

    return redirect("task_list")


@login_required
def task_list_detail(request: HttpRequest, task_list_slug: str):
    """
    Displays the details of a specific task list, including its tasks.

    Args:
        request (HttpRequest): The HTTP request object.
        task_list_id (uuid.UUID): The ID of the task list to display.

    Returns:
        HttpResponse: Renders the task list detail page with tasks.
    """
    try:
        task_list = TaskList.objects.get(slug=task_list_slug, is_deleted=False)
        tasks = (
            Task.objects.filter(task_list=task_list, is_deleted=False)
            .select_related("assigned_to", "created_by", "updated_by")
            .order_by("priority", "created_at")
        )

        # Create task forms for each task
        task_forms = {}
        for task in tasks:
            task_forms[task.id] = TaskForm(instance=task)

        return render(
            request,
            "core/task_list_detail.html",
            {
                "task_list": task_list,
                "tasks": tasks,
                "completed_count": tasks.filter(completed=True).count(),
                "pending_count": tasks.filter(completed=False).count(),
                "task_forms": task_forms,
            },
        )
    except TaskList.DoesNotExist:
        messages.error(request, "Task list not found.")
        return redirect("task_list")


@login_required
def task_edit(request: HttpRequest, task_slug: str):
    if request.method == "POST":
        try:
            task = Task.objects.get(slug=task_slug, is_deleted=False)
            form = TaskForm(request.POST, instance=task)

            if form.is_valid():
                task: Task = form.save(commit=False)
                task.updated_by = request.user
                task.save()
                messages.success(request, "Task updated successfully.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            return redirect("core:task_list_detail", task_list_slug=task.task_list.slug)

        except Task.DoesNotExist:
            messages.error(request, "Task not found.")
    else:
        try:
            task = Task.objects.get(slug=task_slug, is_deleted=False)
            form = TaskForm(instance=task)
            return render(request, "core/task_edit.html", {"form": form, "task": task})

        except Task.DoesNotExist:
            messages.error(request, "Task not found.")
            return redirect("task_list")


@login_required
def task_delete(request: HttpRequest, task_slug: str):
    """
    Deletes a task from a task list.

    Args:
        request (HttpRequest): The HTTP request object.
        task_slug (str): The slug of the task to delete.

    Returns:
        HttpResponse: Redirects to the task list detail page with a success message.
    """
    try:
        task: Task = Task.objects.get(slug=task_slug, is_deleted=False)
        task.is_deleted = True
        task.save()
        messages.success(request, "Task deleted successfully.")
    except Task.DoesNotExist:
        messages.error(request, "Task not found.")
    return redirect("task_list_detail", task_list_slug=task.task_list.slug)


@login_required
def download_template(request: HttpRequest):
    """
    Generates and returns an Excel file template for task import.

    This view creates a sample task list as a Polars DataFrame, writes it to an Excel file in memory,
    and returns it as an HTTP response with appropriate headers for file download.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: An HTTP response containing the Excel file as an attachment.
    """

    df = pl.DataFrame(
        data={
            "task_list_name": ["Wedding Venue", "Wedding Venue", "Catering", "Photography"],
            "title": ["Book ceremony location", "Book reception venue", "Choose menu options", "Hire photographer"],
            "description": [
                "Find and book the perfect ceremony location",
                "Reserve reception venue for 100 guests",
                "Select appetizers and main courses",
                "Find professional wedding photographer",
            ],
            "due_date": ["2024-03-15", "2024-03-20", "2024-04-01", "2024-02-28"],
            "priority": [1, 1, 2, 1],
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
    response["Content-Disposition"] = 'attachment; filename="task_import_template.xlsx"'

    return response


@login_required
def task_create(request: HttpRequest, task_list_slug: str):
    """
    Create a new task.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the task list detail page with a success message.
    """
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task: Task = form.save(commit=False)
            task.task_list = TaskList.objects.get(slug=task_list_slug, is_deleted=False)
            if not task.task_list:
                messages.error(request, "Task list not found.")
                return redirect("task_list")
            task.created_by = request.user
            task.updated_by = request.user
            task.slug = slugify(task.title)
            task.save()
            messages.success(request, "Task created successfully.")
            return redirect("core:task_list_detail", task_list_slug=task_list_slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("core:task_list_detail", task_list_slug=task_list_slug)
    else:
        task_list = TaskList.objects.get(slug=task_list_slug, is_deleted=False)
        if not task_list:
            messages.error(request, "Task list not found.")
            return redirect("task_list")
        return render(request, "core/task_create.html", {"form": TaskForm(), "task_list": task_list})


@login_required
def idea_list(request: HttpRequest):
    """
    Render the 'Idea List' page of the application.
    """
    ideas = Idea.objects.filter(is_deleted=False).select_related("created_by", "updated_by").order_by("created_at")
    add_idea_form = IdeaForm()
    return render(request, "core/idea_list.html", {"ideas": ideas, "add_idea_form": add_idea_form})


@login_required
def idea_create(request: HttpRequest):
    """
    Create a new idea.
    """
    if request.method == "POST":
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea: Idea = form.save(commit=False)
            idea.created_by = request.user
            idea.updated_by = request.user
            idea.save()
            messages.success(request, "Idea created successfully.")
            return redirect("core:idea_detail", idea_slug=idea.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return render(request, "core/idea_create.html", context={"form": IdeaForm()})


@login_required
def idea_detail(request: HttpRequest, idea_slug: str):
    """
    Display the details of a specific idea.

    Args:
        request (HttpRequest): The HTTP request object.
        idea_slug (str): The slug of the idea to display.

    Returns:
        HttpResponse: Renders the idea detail page.
    """
    try:
        idea = Idea.objects.get(slug=idea_slug, is_deleted=False)
        return render(request, "core/idea_detail.html", {"idea": idea})
    except Idea.DoesNotExist:
        messages.error(request, "Idea not found.")
        return redirect("idea_list")


@login_required
def idea_delete(request: HttpRequest, idea_slug: str):
    """
    Deletes an idea.

    Args:
        request (HttpRequest): The HTTP request object.
        idea_slug (str): The slug of the idea to delete.

    Returns:
        HttpResponse: Redirects to the idea list page with a success message.
    """
    logger.error(f"Deleting idea: {idea_slug}")
    try:
        idea = Idea.objects.get(slug=idea_slug, is_deleted=False)
        idea.is_deleted = True
        idea.save()
        messages.success(request, "Idea deleted successfully.")
    except Idea.DoesNotExist:
        messages.error(request, "Idea not found.")
    return redirect("core:idea_list")


@login_required
def idea_edit(request: HttpRequest, idea_slug: str):
    """
    Edits an existing idea.

    Args:
        request (HttpRequest): The HTTP request object.
        idea_slug (str): The slug of the idea to edit.

    Returns:
        HttpResponse: Redirects to the idea detail page with a success message.
    """
    if request.method == "POST":
        try:
            idea = Idea.objects.get(slug=idea_slug, is_deleted=False)
            form = IdeaForm(request.POST, instance=idea)

            if form.is_valid():
                idea: Idea = form.save(commit=False)
                idea.updated_by = request.user
                idea.save()
                messages.success(request, "Idea updated successfully.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            return redirect("core:idea_detail", idea_slug=idea.slug)
        except Idea.DoesNotExist:
            messages.error(request, "Idea not found.")
            return redirect("idea_list")
    # If GET request, show the edit form
    else:
        idea = Idea.objects.get(slug=idea_slug, is_deleted=False)
        form = IdeaForm(instance=idea)
        return render(request, "core/idea_edit.html", {"form": form, "idea": idea})


def idea_import(request: HttpRequest):
    if request.method == "POST":
        form = IdeaImportForm(request.POST, request.FILES)
        excel_file = request.FILES.get("excel_file")

        if not excel_file:
            messages.error(request, "Please select an Excel file to upload.")
            return redirect("contacts:list")

        if form.is_valid():
            df = pl.read_excel(io.BytesIO(excel_file.read()))
            # Validate required columns
            required_columns = ["name"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                messages.error(request, f"Missing required columns: {', '.join(missing_columns)}")
                return redirect("idea:list")

            created_count = 0
            updated_count = 0
            error_count = 0

            for row in df.to_dicts():
                try:
                    name = row.get("name", "").strip()
                    description = row.get("description", "").strip() if row.get("description") else ""

                    # Check if idea already exists
                    idea, created = Idea.objects.update_or_create(
                        slug=slugify(name),
                        defaults={
                            "name": name,
                            "description": description,
                            "created_by": request.user,
                            "updated_by": request.user,
                            "is_deleted": False,
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as e:
                    error_count += 1
                    continue

            # Success message
            message_parts = []
            if created_count > 0:
                message_parts.append(f"{created_count} contact{'s' if created_count != 1 else ''} created")
            if updated_count > 0:
                message_parts.append(f"{updated_count} contact{'s' if updated_count != 1 else ''} updated")

            if message_parts:
                messages.success(request, f"Import completed: {', '.join(message_parts)}.")

            if error_count > 0:
                messages.warning(request, f"{error_count} row{'s' if error_count != 1 else ''} skipped due to errors.")

            return redirect("core:idea_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = IdeaImportForm()
    return render(request, "core/idea_import.html", {"form": form})


def idea_template_download(request: HttpRequest):
    """
    Generates and returns an Excel file template for idea import.

    This view creates a sample idea list as a Polars DataFrame, writes it to an Excel file in memory,
    and returns it as an HTTP response with appropriate headers for file download.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: An HTTP response containing the Excel file as an attachment.
    """
    df = pl.DataFrame(
        data={
            "name": ["Wedding Venue", "Catering", "Photography"],
            "description": [
                "Find and book the perfect ceremony location",
                "Select appetizers and main courses",
                "Hire professional wedding photographer",
            ],
        }
    )
    output = io.BytesIO()
    df.write_excel(output)
    output.seek(0)

    # Create the HTTP response with the Excel file
    response = HttpResponse(
        output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="idea_import_template.xlsx"'

    return response


@csrf_exempt
@require_POST
def csp_report(request):
    """Handle CSP violation reports"""
    try:
        report = json.loads(request.body.decode("utf-8"))
        logger.warning(f"CSP Violation: {report}")
    except (ValueError, UnicodeDecodeError) as e:
        logger.error(f"Failed to parse CSP report: {e}")

    return HttpResponse(status=204)
