import datetime
import io
import json
import logging
from decimal import Decimal

import polars as pl
from attachments.forms import AttachmentUploadForm
from attachments.models import Attachment
from deadline.models import Deadline
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from expenses.models import Category
from expenses.models import Expense
from guestlist.models import Guest
from guestlist.models import GuestGroup
from list.models import List
from list.models import ListEntry

from .forms import IdeaForm
from .forms import IdeaImportForm
from .forms import InspirationForm
from .forms import QuestionForm
from .forms import TimelineForm
from .forms import TimelineImportForm
from .forms import WeddingSettingsForm
from .models import Idea
from .models import Inspiration
from .models import Question
from .models import Timeline
from .models import WeddingSettings

logger = logging.getLogger(__name__)


def home(request: HttpRequest) -> HttpResponse:
    """
    Render the main page of the application.
    """
    return render(request, "core/index.html")


def venue(request: HttpRequest) -> HttpResponse:
    """
    Render the venues page of the application.
    """
    timeline = Timeline.objects.filter(is_deleted=False, published=True).order_by("start")
    return render(request, "core/venue.html", {"timeline": timeline})


def our_story(request: HttpRequest) -> HttpResponse:
    """
    Render the 'Our Story' page of the application.
    """
    return render(request, "core/our_story.html")


def rsvp(request: HttpRequest) -> HttpResponse:
    """
    Render the 'RSVP' page of the application.
    """
    settings = WeddingSettings.load()
    logger.error(settings.allow_rsvp)
    context = {}
    if settings.allow_rsvp:
        context = {"test": "value"}

    return render(request, "core/rsvp.html", context)


def photos(request: HttpRequest) -> HttpResponse:
    """
    Render the 'Photos' page of the application.
    """
    return render(request, "core/photos.html")


def faq(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.filter(is_deleted=False, published=True).order_by("order").order_by("question")
    return render(request, "core/faq.html", {"questions": questions})


@login_required
def idea_list(request: HttpRequest) -> HttpResponse:
    """
    Render the 'Idea List' page of the application.
    """
    ideas = Idea.objects.filter(is_deleted=False).select_related("created_by", "updated_by").order_by("created_at")
    return render(
        request,
        "core/idea_list.html",
        {
            "ideas": ideas,
            "delete_modal_url": reverse("core:idea_delete_modal"),
        },
    )


@login_required
def idea_create(request: HttpRequest) -> HttpResponse:
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
    return render(request, "form/object.html", context)


@login_required
def idea_detail(request: HttpRequest, idea_slug: str) -> HttpResponse:
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
    return render(request, "components/modal/object_delete_modal_body.html", context)


@login_required
def idea_delete(request: HttpRequest, idea_slug: str) -> HttpResponse:
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
def idea_edit(request: HttpRequest, idea_slug: str) -> HttpResponse:
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
    return render(request, "form/object.html", context)


@login_required
def idea_import(request: HttpRequest) -> HttpResponse:
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
                        name=name,
                        defaults={
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

                except Exception:
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
def idea_template_download(request: HttpRequest) -> HttpResponse:
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
def csp_report(request) -> HttpResponse:
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

    context = {
        "timeline_events": True if Timeline.objects.filter(is_deleted=False) else False,
        "delete_modal_url": reverse("core:timeline_delete_modal"),
    }

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
        menu_content = render_to_string(
            "cotton/table/row_actions.html",
            {
                "detail_url": reverse("core:timeline_detail", args=[event.slug]),
                "update_url": reverse("core:timeline_edit", args=[event.slug]),
                "slug": event.slug,
            },
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
    try:
        timeline_event = Timeline.objects.get(slug=timeline_slug, is_deleted=False)
    except Timeline.DoesNotExist:
        messages.error(request, "Timeline event not found.")
        return redirect("core:timeline_summary")

    breadcrumbs = [
        {"title": "Timeline", "url": reverse("core:timeline_summary")},
        {"title": f"{timeline_event}", "url": None},
    ]

    # Calculate duration if both start and end dates exist
    duration = None
    if timeline_event.start and timeline_event.end:
        duration = timeline_event.end - timeline_event.start

    context = {
        "timeline_event": timeline_event,
    }
    context = {
        "block_title": f"{timeline_event}",
        "breadcrumbs": breadcrumbs,
        "title": f"{timeline_event}",
        "object": timeline_event,
        "edit_url": reverse("core:timeline_edit", args=[timeline_event.slug]),
        "link_url": None,
        "image_url": None,
        "status": timeline_event.confirmed,
        "status_text": "Confirmed" if timeline_event.confirmed else "Pending Confirmation",
        "delete_modal_url": reverse("core:timeline_delete_modal"),
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
    return render(request, "form/object.html", context)


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
    return render(request, "form/object.html", context)


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
    return render(request, "components/modal/object_delete_modal_body.html", context)


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
    buffer = io.BytesIO()
    df.write_excel(buffer)
    buffer.seek(0)

    # Return as downloadable file
    response = HttpResponse(
        buffer.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="timeline_import_template.xlsx"'
    return response


@login_required
def inspiration_summary(request: HttpRequest) -> HttpResponse:
    """
    Render the 'Inspiration Summary' page of the application.
    """

    inspirations = Inspiration.objects.filter(is_deleted=False).order_by("created_at")
    context = {"inspirations": inspirations, "form": InspirationForm()}
    return render(request, "core/inspiration_summary.html", context)


@login_required
def inspiration_create(request: HttpRequest) -> HttpResponse:
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
    return render(request, "form/object.html", context)


@login_required
def inspiration_detail(request: HttpRequest, inspiration_slug: str) -> HttpResponse:
    """
    Display the details of a specific inspiration.

    Args:
        request (HttpRequest): The HTTP request object.
        inspiration_slug (str): The slug of the inspiration to display.

    Returns:
        HttpResponse: Rendered template with inspiration details.
    """
    try:
        inspiration = Inspiration.objects.get(slug=inspiration_slug, is_deleted=False)

    except Inspiration.DoesNotExist:
        messages.error(request, "Inspiration not found.")
        return redirect("inspiration_list")

    breadcrumbs = [
        {"title": "Inspiration Board", "url": reverse("core:inspiration_summary")},
        {"title": f"{inspiration}", "url": None},
    ]
    attach_url_query = QueryDict("", mutable=True)
    attach_url_query["next"] = request.path
    context = {
        "block_title": f"{inspiration}",
        "breadcrumbs": breadcrumbs,
        "title": f"{inspiration}",
        "object": inspiration,
        "edit_url": reverse("core:inspiration_edit", args=[inspiration.slug]),
        "status": None,
        "status_text": None,
        "link_url": None,
        "image_url": None,
        "delete_modal_url": reverse("core:inspiration_delete_modal"),
        "attachments": Attachment.objects.attachments_for_object(inspiration).all(),
        "attach_form": AttachmentUploadForm(),
        "attach_submit_url": str(
            reverse(
                "attachments:add_attachment",
                kwargs={"app_label": "core", "model_name": "Inspiration", "pk": inspiration.pk},
                query=attach_url_query,
            )
        ),
    }

    return render(request, "core/inspiration_detail.html", context)


@login_required
def inspiration_edit(request: HttpRequest, inspiration_slug: str) -> HttpResponse:
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
    return render(request, "form/object.html", context)


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
    return render(request, "components/modal/object_delete_modal_body.html", context)


@login_required
def inspiration_delete(request: HttpRequest, inspiration_slug: str) -> HttpResponse:
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


@login_required
def question_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question: Question = form.save(commit=False)
            question.created_by = request.user
            question.updated_by = request.user
            question.save()
            messages.success(request, "Question created successfully.")
            return redirect("core:question_detail", question_slug=question.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = QuestionForm()
    intro = "Create a new question for the FAQ Page"
    breadcrumbs = [
        {"title": "Questions", "url": reverse("core:question_summary")},
        {"title": "New Question", "url": None},
    ]
    cancel_url = reverse("core:question_summary")
    context = {
        "block_title": "New Question",
        "breadcrumbs": breadcrumbs,
        "title": "New Question",
        "intro": intro,
        "form": form,
        "object": None,
        "submit_text": "Create",
        "cancel_url": cancel_url,
        "first_field": "question",
        "file": False,
        "hugerte_enabled": True,
        "selector": "id_answer",
    }
    return render(request, "form/object.html", context)


@login_required
def question_edit(request: HttpRequest, question_slug: str) -> HttpResponse:
    question = get_object_or_404(Question, slug=question_slug, is_deleted=False)
    try:
        question = Question.objects.get(slug=question_slug, is_deleted=False)

    except Question.DoesNotExist:
        messages.error(request, "Question not found.")
        return redirect("core:question_summary")

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.updated_by = request.user
            question.save()
            messages.success(request, "Question updated successfully.")
            return redirect("core:question_detail", question_slug=question.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = QuestionForm(instance=question)

    intro = "Edit an existing question"
    breadcrumbs = [
        {"title": "Questions", "url": reverse("core:question_summary")},
        {"title": question, "url": reverse("core:question_detail", args=[question.slug])},
    ]
    cancel_url = reverse("core:question_detail", args=[question.slug])
    context = {
        "block_title": "Edit Question",
        "breadcrumbs": breadcrumbs,
        "title": "Edit Question",
        "intro": intro,
        "form": form,
        "object": None,
        "submit_text": "Update",
        "cancel_url": cancel_url,
        "first_field": "question",
        "file": False,
        "hugerte_enabled": True,
        "selector": "id_answer",
    }
    return render(request, "form/object.html", context)


@login_required
def question_delete_modal(request: HttpRequest) -> HttpResponse | JsonResponse:
    question_slug = request.GET.get("slug")
    if not question_slug:
        return JsonResponse({"error": "Question slug is required"}, status=400)
    try:
        question = Question.objects.get(slug=question_slug, is_deleted=False)
    except Question.DoesNotExist:
        return JsonResponse({"error": "Question not found"}, status=404)

    context = {
        "object": question,
        "object_type": "Question",
        "action_url": reverse("core:question_delete", args=[question.slug]),
    }
    return render(request, "components/modal/object_delete_modal_body.html", context)


@login_required
def question_delete(request: HttpRequest, question_slug: str) -> HttpResponse:
    question = get_object_or_404(Question, slug=question_slug, is_deleted=False)
    try:
        question = Question.objects.get(slug=question_slug, is_deleted=False)

    except Question.DoesNotExist:
        messages.error(request, "Question not found.")
        return redirect("core:question_summary")

    if request.method == "POST":
        question.is_deleted = True
        question.updated_by = request.user
        question.save()
        messages.success(request, f"Question '{question}' deleted successfully.")
        return redirect("core:question_summary")
    else:
        messages.error(request, "Invalid request method. Please use POST to delete a question.")
        return redirect("core:question_detail", question_slug=question.slug)


@login_required
def question_detail(request: HttpRequest, question_slug: str) -> HttpResponse:
    try:
        question = Question.objects.get(slug=question_slug, is_deleted=False)

    except Question.DoesNotExist:
        messages.error(request, "Question not found.")
        return redirect("core:question_summary")

    breadcrumbs = [
        {"title": "FAQ", "url": reverse("core:question_summary")},
        {"title": f"{question}", "url": None},
    ]
    attach_url_query = QueryDict("", mutable=True)
    attach_url_query["next"] = request.path
    context = {
        "block_title": f"{question}",
        "breadcrumbs": breadcrumbs,
        "title": f"{question}",
        "object": question,
        "edit_url": reverse("core:question_edit", args=[question.slug]),
        "status": None,
        "status_text": None,
        "link_url": None,
        "image_url": None,
        "delete_modal_url": reverse("core:question_delete_modal"),
        "attachments": Attachment.objects.attachments_for_object(question).all(),
        "attach_form": AttachmentUploadForm(),
        "attach_submit_url": str(
            reverse(
                "attachments:add_attachment",
                kwargs={"app_label": "core", "model_name": "Question", "pk": question.pk},
                query=attach_url_query,
            )
        ),
    }
    return render(request, "core/question_detail.html", context)


@login_required
def question_summary(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.filter(is_deleted=False).order_by("created_at")
    context = {"questions": questions, "form": QuestionForm()}
    return render(request, "core/question_summary.html", context)


@login_required
def planning_home(request: HttpRequest) -> HttpResponse:
    """
    Render the 'Planning Home' page with comprehensive wedding planning summary.
    """

    now = datetime.datetime.now()

    # Budget & Expenses data
    expenses = Expense.objects.filter(is_deleted=False)
    total_estimated = expenses.aggregate(total=Sum("estimated_amount"))["total"] or Decimal("0.00")
    total_actual = expenses.aggregate(total=Sum("actual_amount"))["total"] or Decimal("0.00")
    expense_count = expenses.count()
    category_count = Category.objects.filter(is_deleted=False).count()
    purchased_count = expenses.filter(actual_amount__isnull=False).count()

    # Guest List data
    guests = Guest.objects.filter(is_deleted=False)
    guest_groups = GuestGroup.objects.filter(is_deleted=False)
    guest_count = guests.count()
    guest_group_count = guest_groups.count()
    invited_guests = guests.filter(is_invited=True).count()
    declined_guests = guests.filter(is_attending=False, responded=True, is_invited=True).count()
    confirmed_guests = guests.filter(is_attending=True, responded=True, is_invited=True).count()
    pending_guests = guests.filter(responded=False, is_invited=True).count()

    # Timeline data
    timelines = Timeline.objects.filter(is_deleted=False)
    timeline_count = timelines.count()
    confirmed_timeline = timelines.filter(confirmed=True).count()
    published_timeline = timelines.filter(published=True).count()

    # TODO Chnage logic to get next event
    settings = WeddingSettings.load()
    if settings.wedding_date:
        wedding_date = settings.wedding_date
        days_until_wedding = (wedding_date - now.date()).days
    else:
        days_until_wedding = 0

    # Deadlines data
    deadlines = Deadline.objects.filter(is_deleted=False)
    deadline_count = deadlines.count()
    upcoming_deadlines = deadlines.filter(due_date__gte=now, completed=False).count()
    completed_deadlines = deadlines.filter(completed=True).count()

    # Lists data
    lists = List.objects.filter(is_deleted=False)
    list_entries = ListEntry.objects.filter(is_deleted=False)
    list_count = lists.count()
    list_entry_count = list_entries.count()
    completed_entries = list_entries.filter(is_completed=True).count()

    # Recent Activity
    upcoming_deadline_items = deadlines.filter(
        due_date__gte=now, due_date__lte=now + datetime.timedelta(days=30), completed=False
    ).order_by("due_date")[:5]

    context = {
        # Budget stats
        "total_estimated": total_estimated,
        "total_actual": total_actual,
        "expense_count": expense_count,
        "category_count": category_count,
        "purchased_count": purchased_count,
        # Guest stats
        "guest_count": guest_count,
        "guest_group_count": guest_group_count,
        "confirmed_guests": confirmed_guests,
        "declined_guests": declined_guests,
        "pending_guests": pending_guests,
        "invited_guests": invited_guests,
        # Timeline stats
        "timeline_count": timeline_count,
        "confirmed_timeline": confirmed_timeline,
        "published_timeline": published_timeline,
        "days_until_wedding": days_until_wedding,
        # Deadline stats
        "deadline_count": deadline_count,
        "upcoming_deadlines": upcoming_deadlines,
        "completed_deadlines": completed_deadlines,
        # List stats
        "list_count": list_count,
        "list_entry_count": list_entry_count,
        "completed_entries": completed_entries,
        # Recent activity
        "upcoming_deadline_items": upcoming_deadline_items,
    }

    return render(request, "core/planning_home.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def wedding_settings_edit(request):
    settings = WeddingSettings.load()

    context = {
        "breadcrumbs": [
            {"title": "Planning", "url": reverse("core:planning_home")},
            {"title": "Wedding Settings", "url": reverse("core:wedding_settings")},
            {"title": "Edit", "url": None},
        ],
        "block_title": "Edit Wedding Settings",
        "title": "Edit Wedding Settings",
        "settings_form": WeddingSettingsForm(instance=settings),
        "cancel_url": reverse("core:wedding_settings"),
        "submit_text": "Update Settings",
    }
    if request.method == "POST":
        form = WeddingSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.updated_by = request.user
            settings.save()
            messages.success(request, "Wedding settings updated successfully.")
        return redirect("core:wedding_settings")
    return render(request, "core/wedding_settings_form.html", context)


def wedding_settings(request):
    settings = WeddingSettings.load()
    context = {
        "block_title": "Wedding Settings",
        "breadcrumbs": [
            {"title": "Planning", "url": reverse("core:planning_home")},
            {"title": "Wedding Settings", "url": None},
        ],
        "title": "Wedding Settings",
        "edit_url": reverse("core:wedding_settings_edit"),
        "settings": settings,
    }
    return render(request, "core/wedding_settings_detail.html", context)
