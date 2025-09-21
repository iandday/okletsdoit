import datetime
import io
import json
import logging
from io import BytesIO

import polars as pl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, QueryDict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from attachments.forms import AttachmentUploadForm
from attachments.models import Attachment
from shared_helpers.table_helpers import format_row_action_cell

from core.forms import IdeaForm
from core.forms import IdeaImportForm
from core.forms import InspirationForm
from core.forms import TimelineForm
from core.forms import TimelineImportForm
from core.models import Idea

from .models import Inspiration
from .models import Timeline

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
    timeline = Timeline.objects.filter(is_deleted=False, published=True).order_by("start")
    return render(request, "core/venue.html", {"timeline": timeline})


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
def idea_list(request: HttpRequest):
    """
    Render the 'Idea List' page of the application.
    """
    ideas = Idea.objects.filter(is_deleted=False).select_related("created_by", "updated_by").order_by("created_at")
    add_idea_form = IdeaForm()
    return render(
        request,
        "core/idea_list.html",
        {
            "ideas": ideas,
            "add_idea_form": add_idea_form,
            "delete_modal_url": reverse("core:idea_delete_modal"),
        },
    )


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
    else:
        form = IdeaForm()
    intro = "Create an idea"
    breadcrumbs = [
        {"title": "Ideas", "url": reverse("core:idea_list")},
        {"title": "Create", "url": reverse("core:idea_create")},
    ]
    cancel_url = reverse("core:idea_list")
    context = {
        "block_title": "Create Idea",
        "breadcrumbs": breadcrumbs,
        "title": "Create Idea",
        "intro": intro,
        "form": form,
        "submit_text": "Create Idea",
        "cancel_url": cancel_url,
        "first_field": "name",
        "hugerte_enabled": True,
        "selector": "id_description",
    }
    return render(request, "shared_helpers/form/object.html", context)


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

    except Idea.DoesNotExist:
        messages.error(request, "Idea not found.")
        return redirect("idea_list")

    breadcrumbs = [
        {"title": "Ideas", "url": reverse("core:idea_list")},
        {"title": f"{idea}", "url": None},
    ]
    attach_url_query = QueryDict("", mutable=True)
    attach_url_query["next"] = request.path
    context = {
        "block_title": f"{idea}",
        "breadcrumbs": breadcrumbs,
        "title": f"{idea}",
        "object": idea,
        "edit_url": reverse("core:idea_edit", args=[idea.slug]),
        "status": None,
        "status_text": None,
        "link_url": None,
        "image_url": None,
        "delete_modal_url": reverse("core:idea_delete_modal"),
        "attachments": Attachment.objects.attachments_for_object(idea).all(),
        "attach_form": AttachmentUploadForm(),
        "attach_submit_url": str(
            reverse(
                "attachments:add_attachment",
                kwargs={"app_label": "core", "model_name": "Idea", "pk": idea.pk},
                query=attach_url_query,
            )
        ),
    }
    return render(request, "core/idea_detail.html", context)


@login_required
def idea_delete_modal(request: HttpRequest) -> HttpResponse | JsonResponse:
    idea_slug = request.GET.get("slug")
    if not idea_slug:
        return JsonResponse({"error": "Idea slug is required"}, status=400)
    try:
        idea = Idea.objects.get(slug=idea_slug, is_deleted=False)
    except Idea.DoesNotExist:
        return JsonResponse({"error": "Idea not found"}, status=404)

    context = {
        "object": idea,
        "object_type": "Idea",
        "action_url": reverse("core:idea_delete", args=[idea.slug]),
    }
    return render(request, "shared_helpers/modal/object_delete_body.html", context)


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
    idea = get_object_or_404(Idea, slug=idea_slug, is_deleted=False)

    if request.method == "POST":
        idea.is_deleted = True
        idea.updated_by = request.user
        idea.save()
        messages.success(request, f"Idea '{idea.name}' deleted successfully.")
    else:
        messages.error(request, "Invalid request method.")

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
    idea = get_object_or_404(Idea, slug=idea_slug, is_deleted=False)

    if request.method == "POST":
        form = IdeaForm(request.POST, instance=idea)

        if form.is_valid():
            idea: Idea = form.save(commit=False)
            idea.updated_by = request.user
            idea.save()
            messages.success(request, "Idea updated successfully.")
            return redirect("core:idea_detail", idea_slug=idea.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = IdeaForm(instance=idea)
    intro = "Edit an idea"
    breadcrumbs = [
        {"title": "Ideas", "url": reverse("core:idea_list")},
        {"title": idea.name, "url": reverse("core:idea_detail", args=[idea.slug])},
    ]
    cancel_url = reverse("core:idea_detail", args=[idea.slug])
    context = {
        "block_title": "Edit Idea",
        "breadcrumbs": breadcrumbs,
        "title": "Edit Idea",
        "intro": intro,
        "form": form,
        "object": idea,
        "submit_text": "Update",
        "cancel_url": cancel_url,
        "first_field": "name",
        "hugerte_enabled": True,
        "selector": "id_description",
    }
    return render(request, "shared_helpers/form/object.html", context)


@login_required
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


@login_required
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


@login_required
def timeline_summary(request: HttpRequest) -> HttpResponse:
    """
    Displays the summary of timeline events.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template with timeline events summary.
    """

    context = {"timeline_events": True if Timeline.objects.filter(is_deleted=False) else False}

    return render(request, "core/timeline_summary.html", context)


@login_required
def timeline_data(request) -> JsonResponse:
    """
    Provides timeline events data in JSON format for frontend consumption.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing timeline events data.
    """
    # Get DataTables parameters
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")

    # Handle sorting
    order_column_index = request.GET.get("order[0][column]")
    order_direction = request.GET.get("order[0][dir]")
    order_column_name = request.GET.get(f"columns[{order_column_index}][name]")

    queryset = Timeline.objects.filter(is_deleted=False)

    records_total = queryset.count()

    # Apply search filter if provided
    if search_value:
        queryset = queryset.filter(Q(name__icontains=search_value) | Q(description__icontains=search_value))
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

    data = []
    for event in queryset:
        menu_content = format_row_action_cell(
            detail_url=reverse("core:timeline_detail", args=[event.slug]),
            update_url=reverse("core:timeline_edit", args=[event.slug]),
            slug=event.slug,
        )

        data.append(
            {
                "name": event.name,
                "start": event.start,
                "end": event.end,
                "status": "Confirmed" if event.confirmed else "Pending",
                "published": "Published" if event.published else "Draft",
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
def timeline_detail(request: HttpRequest, timeline_slug: str) -> HttpResponse:
    """
    Display the details of a specific timeline event.

    Args:
        request (HttpRequest): The HTTP request object.
        timeline_slug (str): The slug of the timeline event to display.

    Returns:
        HttpResponse: Rendered template with timeline event details.
    """
    timeline_event = get_object_or_404(Timeline, slug=timeline_slug, is_deleted=False)

    # Calculate duration if both start and end dates exist
    duration = None
    if timeline_event.start and timeline_event.end:
        duration = timeline_event.end - timeline_event.start

    context = {
        "timeline_event": timeline_event,
        "duration_days": duration.days if duration else None,
        "duration_hours": duration.seconds // 3600 if duration else None,
        "duration_minutes": (duration.seconds // 60) % 60 if duration else None,
        "duration_seconds": duration.seconds % 60 if duration else None,
        "duration": duration,
    }

    return render(request, "core/timeline_detail.html", context)


@login_required
def timeline_create(request: HttpRequest) -> HttpResponse:
    """
    Create a new timeline event.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template or redirect response.
    """
    if request.method == "POST":
        form = TimelineForm(request.POST)
        if form.is_valid():
            timeline_event = form.save(commit=False)
            timeline_event.created_by = request.user
            timeline_event.updated_by = request.user
            timeline_event.save()
            messages.success(request, "Timeline event created successfully.")
            return redirect("core:timeline_detail", timeline_slug=timeline_event.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = TimelineForm()
    intro = "Create a new timeline event"
    breadcrumbs = [
        {"title": "Timeline", "url": reverse("core:timeline_summary")},
        {"title": "Create Event", "url": None},
    ]
    cancel_url = reverse("core:timeline_summary")
    context = {
        "block_title": "Create Event",
        "breadcrumbs": breadcrumbs,
        "title": "Create Event",
        "intro": intro,
        "form": form,
        "object": None,
        "submit_text": "Create Event",
        "cancel_url": cancel_url,
        "first_field": "name",
    }
    return render(request, "shared_helpers/form/object.html", context)


@login_required
def timeline_edit(request: HttpRequest, timeline_slug: str) -> HttpResponse:
    """
    Edit an existing timeline event.

    Args:
        request (HttpRequest): The HTTP request object.
        timeline_slug (str): The slug of the timeline event to edit.

    Returns:
        HttpResponse: Rendered template or redirect response.
    """
    timeline_event = get_object_or_404(Timeline, slug=timeline_slug, is_deleted=False)

    if request.method == "POST":
        form = TimelineForm(request.POST, instance=timeline_event)
        if form.is_valid():
            timeline_event = form.save(commit=False)
            timeline_event.updated_by = request.user
            timeline_event.save()
            messages.success(request, "Timeline event updated successfully.")
            return redirect("core:timeline_detail", timeline_slug=timeline_event.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = TimelineForm(instance=timeline_event)

    intro = "Edit an existing timeline event"
    breadcrumbs = [
        {"title": "Timeline", "url": reverse("core:timeline_summary")},
        {"title": timeline_event, "url": reverse("core:timeline_detail", args=[timeline_event.slug])},
    ]
    cancel_url = reverse("core:timeline_detail", args=[timeline_event.slug])
    context = {
        "block_title": "Edit Event",
        "breadcrumbs": breadcrumbs,
        "title": "Edit Event",
        "intro": intro,
        "form": form,
        "object": None,
        "submit_text": "Update Event",
        "cancel_url": cancel_url,
        "first_field": "name",
    }
    return render(request, "shared_helpers/form/object.html", context)


@login_required
def timeline_delete_modal(request: HttpRequest) -> HttpResponse | JsonResponse:
    timeline_slug = request.GET.get("slug")
    if not timeline_slug:
        return JsonResponse({"error": "Timeline slug is required"}, status=400)
    try:
        timeline_event = Timeline.objects.get(slug=timeline_slug, is_deleted=False)
    except Timeline.DoesNotExist:
        return JsonResponse({"error": "Timeline not found"}, status=404)

    context = {
        "object": timeline_event,
        "object_type": "Timeline entry",
        "action_url": reverse("core:timeline_delete", args=[timeline_event.slug]),
    }
    return render(request, "shared_helpers/modal/object_delete_body.html", context)


@login_required
def timeline_delete(request: HttpRequest, timeline_slug: str) -> HttpResponse:
    """
    Delete a timeline event by marking it as deleted.

    Args:
        request (HttpRequest): The HTTP request object.
        timeline_slug (str): The slug of the timeline event to delete.

    Returns:
        HttpResponse: Rendered confirmation template or redirect response.
    """
    timeline_event = get_object_or_404(Timeline, slug=timeline_slug, is_deleted=False)

    if request.method == "POST":
        timeline_event.is_deleted = True
        timeline_event.updated_by = request.user
        timeline_event.save()
        messages.success(request, f"Timeline event '{timeline_event.name}' deleted successfully.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect("core:timeline_summary")


@login_required
def timeline_import(request: HttpRequest) -> HttpResponse:
    """
    Handle timeline import via Excel file upload.
    On GET: returns a template spreadsheet for import.
    On POST: processes uploaded Excel file and creates timeline events.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Excel file download (GET) or redirect after processing (POST).
    """

    if request.method == "POST":
        form = TimelineImportForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES.get("excel_file")
            if uploaded_file:
                try:
                    df = pl.read_excel(io.BytesIO(uploaded_file.read()))

                    # Validate required columns
                    required_columns = [
                        "name",
                        "description",
                        "start",
                    ]
                    missing_columns = [col for col in required_columns if col not in df.columns]

                    if missing_columns:
                        messages.error(request, f"Missing required columns: {', '.join(missing_columns)}")
                        return redirect("core:timeline_summary")

                    created_count = 0

                    # Process each row
                    for row in df.iter_rows(named=True):
                        logger.error(f"Processing row: {row}")

                        try:
                            # Parse dates and times

                            start = datetime.datetime.strptime(row["start"], "%Y-%m-%dT%H:%M")
                            logger.error(f"Parsed start time: {row['start']}")
                            if row.get("end", False):
                                end = datetime.datetime.strptime(row["end"], "%Y-%m-%dT%H:%M")
                            else:
                                end = None

                            # Create timeline event
                            timeline_event, created = Timeline.objects.get_or_create(
                                name=str(row["name"]),
                                defaults={
                                    "description": str(row["description"]) if row["description"] else "",
                                    "start": start,
                                    "end": end,
                                    "published": bool(row["published"]) if row["published"] is not None else False,
                                    "confirmed": bool(row["confirmed"]) if row["confirmed"] is not None else False,
                                    "created_by": request.user,
                                    "updated_by": request.user,
                                },
                            )
                            if created:
                                created_count += 1
                            else:
                                # If not created, update existing event
                                timeline_event.description = str(row["description"]) if row["description"] else ""
                                timeline_event.start = start
                                timeline_event.end = end
                                timeline_event.published = (
                                    bool(row["published"]) if row["published"] is not None else False
                                )
                                timeline_event.confirmed = (
                                    bool(row["confirmed"]) if row["confirmed"] is not None else False
                                )
                                timeline_event.updated_by = request.user
                                timeline_event.save()

                        except Exception as e:
                            messages.warning(
                                request, f"Failed to import row with name '{row.get('name', 'Unknown')}': {str(e)}"
                            )
                            continue

                    if created_count > 0:
                        messages.success(request, f"Successfully imported {created_count} timeline events.")
                    else:
                        messages.warning(request, "No timeline events were imported.")

                except Exception as e:
                    messages.error(request, f"Error processing file: {str(e)}")
            else:
                messages.error(request, "Please select an Excel file to upload.")
                return redirect("core:timeline_summary")
        else:
            messages.error(request, "Invalid form submission. Please try again.")

        return redirect("core:timeline_summary")

    # Create template DataFrame with required columns
    template_data = {
        "name": ["Sample Event"],
        "description": ["Sample description for the event"],
        "start": ["2024-01-01T10:00"],
        "end": ["2024-01-01T12:00"],
        "published": [False],
        "confirmed": [True],
    }

    df = pl.DataFrame(template_data)

    # Create Excel file in memory
    buffer = BytesIO()
    df.write_excel(buffer)
    buffer.seek(0)

    # Return as downloadable file
    response = HttpResponse(
        buffer.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="timeline_import_template.xlsx"'
    return response


@login_required
def inspiration_summary(request: HttpRequest):
    """
    Render the 'Inspiration Summary' page of the application.
    """
    if request.method == "POST":
        form = InspirationForm(request.POST, request.FILES)
        if form.is_valid():
            inspiration: Inspiration = form.save(commit=False)
            inspiration.created_by = request.user
            inspiration.updated_by = request.user
            inspiration.save()
            messages.success(request, "Inspiration created successfully.")
        return redirect("core:inspiration_summary")
    else:
        inspirations = Inspiration.objects.filter(is_deleted=False).order_by("created_at")
        context = {"inspirations": inspirations, "form": InspirationForm()}
        return render(request, "core/inspiration_summary.html", context)


@login_required
def inspiration_create(request: HttpRequest):
    """
    Create a new inspiration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template or redirect response.
    """
    if request.method == "POST":
        form = InspirationForm(request.POST, request.FILES)
        if form.is_valid():
            inspiration: Inspiration = form.save(commit=False)
            inspiration.created_by = request.user
            inspiration.updated_by = request.user
            inspiration.save()
            messages.success(request, "Inspiration created successfully.")
            return redirect("core:inspiration_detail", inspiration_slug=inspiration.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = InspirationForm()
    intro = "Upload an existing inspiration"
    breadcrumbs = [
        {"title": "Inspiration", "url": reverse("core:inspiration_summary")},
        {"title": "New Inspiration", "url": None},
    ]
    cancel_url = reverse("core:inspiration_summary")
    context = {
        "block_title": "New Inspiration",
        "breadcrumbs": breadcrumbs,
        "title": "New Inspiration",
        "intro": intro,
        "form": form,
        "object": None,
        "submit_text": "Create",
        "cancel_url": cancel_url,
        "first_field": "name",
        "file": True,
    }
    return render(request, "shared_helpers/form/object.html", context)


@login_required
def inspiration_detail(request: HttpRequest, inspiration_slug: str):
    """
    Display the details of a specific inspiration.

    Args:
        request (HttpRequest): The HTTP request object.
        inspiration_slug (str): The slug of the inspiration to display.

    Returns:
        HttpResponse: Rendered template with inspiration details.
    """
    inspiration = get_object_or_404(Inspiration, slug=inspiration_slug, is_deleted=False)
    return render(request, "core/inspiration_detail.html", {"inspiration": inspiration})


@login_required
def inspiration_edit(request: HttpRequest, inspiration_slug: str):
    """
    Edit an existing inspiration.

    Args:
        request (HttpRequest): The HTTP request object.
        inspiration_slug (str): The slug of the inspiration to edit.

    Returns:
        HttpResponse: Rendered template or redirect response.
    """
    inspiration = get_object_or_404(Inspiration, slug=inspiration_slug, is_deleted=False)

    if request.method == "POST":
        form = InspirationForm(request.POST, request.FILES, instance=inspiration)
        if form.is_valid():
            inspiration = form.save(commit=False)
            inspiration.updated_by = request.user
            inspiration.save()
            messages.success(request, "Inspiration updated successfully.")
            return redirect("core:inspiration_detail", inspiration_slug=inspiration.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = InspirationForm(instance=inspiration)

    intro = "Edit an existing inspiration"
    breadcrumbs = [
        {"title": "Inspiration", "url": reverse("core:inspiration_summary")},
        {"title": inspiration.name, "url": reverse("core:inspiration_detail", args=[inspiration.slug])},
    ]
    cancel_url = reverse("core:inspiration_detail", args=[inspiration.slug])
    context = {
        "block_title": "Edit Inspiration",
        "breadcrumbs": breadcrumbs,
        "title": "Edit Inspiration",
        "intro": intro,
        "form": form,
        "object": None,
        "submit_text": "Update",
        "cancel_url": cancel_url,
        "first_field": "name",
        "file": True,
    }
    return render(request, "shared_helpers/form/object.html", context)


@login_required
def inspiration_delete_modal(request: HttpRequest) -> HttpResponse | JsonResponse:
    inspiration_slug = request.GET.get("slug")
    if not inspiration_slug:
        return JsonResponse({"error": "Inspiration slug is required"}, status=400)
    try:
        inspiration = Inspiration.objects.get(slug=inspiration_slug, is_deleted=False)
    except Inspiration.DoesNotExist:
        return JsonResponse({"error": "Inspiration not found"}, status=404)

    context = {
        "object": inspiration,
        "object_type": "Inspiration",
        "action_url": reverse("core:inspiration_delete", args=[inspiration.slug]),
    }
    return render(request, "shared_helpers/modal/object_delete_body.html", context)


@login_required
def inspiration_delete(request: HttpRequest, inspiration_slug: str):
    """
    Deletes an inspiration by marking it as deleted.

    Args:
        request (HttpRequest): The HTTP request object.
        inspiration_slug (str): The slug of the inspiration to delete.

    Returns:
        HttpResponse: Redirects to the inspiration summary page with a success message.
    """
    inspiration = get_object_or_404(Inspiration, slug=inspiration_slug, is_deleted=False)

    if request.method == "POST":
        inspiration.is_deleted = True
        inspiration.updated_by = request.user
        inspiration.save()
        messages.success(request, f"Inspiration '{inspiration.name}' deleted successfully.")
        return redirect("core:inspiration_summary")
    else:
        messages.error(request, "Invalid request method. Please use POST to delete an inspiration.")
        return redirect("core:inspiration_detail", inspiration_slug=inspiration.slug)
