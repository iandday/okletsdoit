import io
import json
import logging

import polars as pl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.forms import IdeaForm
from core.forms import IdeaImportForm
from core.models import Idea

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

    return render(request, "core/idea_form.html", context={"form": IdeaForm()})


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
        return render(request, "core/idea_form.html", {"form": form, "idea": idea})


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
