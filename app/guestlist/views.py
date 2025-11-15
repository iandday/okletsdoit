import csv
import io
import logging
from typing import Any

import polars as pl
from attachments.forms import AttachmentUploadForm
from attachments.models import Attachment
from core.models import WeddingSettings
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from users.models import User

from .forms import (
    GuestForm,
    GuestRSVPForm,
    RsvpCodeForm,
    RsvpSubmissionForm,
)
from .forms import GuestGroupForm
from .forms import GuestlistImportForm
from .models import Guest, RsvpSubmission
from .models import GuestGroup

logger = logging.getLogger(__name__)


@login_required
def guestlist_import(request: HttpRequest) -> HttpResponse:
    """
    Handles the import of guestlist data from an uploaded Excel file or provides a template for download.
    - On POST:
        - Validates the uploaded Excel file for required columns and data integrity.
        - Processes each row to create or update GuestGroup and Guest instances.
        - Handles errors and provides user feedback via Django messages.
        - Supports both named guests and plus-one entries.
        - Updates existing records if they already exist.
    - On GET:
        - Generates and returns an Excel template file for guestlist import.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Redirects to the guestlist summary page with status messages on POST,
                    or returns an Excel file as an attachment on GET.
    """

    if request.method == "POST":
        form = GuestlistImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get("excel_file")
            if uploaded_file:
                try:
                    df = pl.read_excel(io.BytesIO(uploaded_file.read()))

                    # Validate required columns
                    required_columns = ["group_name", "associated_with", "relationship", "priority"]
                    missing_columns = [col for col in required_columns if col not in df.columns]

                    if missing_columns:
                        messages.error(request, f"Missing required columns: {', '.join(missing_columns)}")
                        return redirect("guestlist:guestlist_summary")

                    # Check if we have either name columns or plus_one column
                    has_name_columns = "first_name" in df.columns and "last_name" in df.columns
                    has_plus_one_column = "plus_one" in df.columns

                    if not has_name_columns and not has_plus_one_column:
                        messages.error(
                            request,
                            "Missing required columns: Either 'first_name' and 'last_name' OR 'plus_one' column must be present",
                        )
                        return redirect("guestlist:guestlist_summary")

                    # Process the data
                    success_count = 0
                    error_count = 0
                    update_count = 0
                    errors = []

                    # Convert to Python dicts for iteration
                    for index, row in enumerate(df.to_dicts()):
                        try:
                            # Get or create guest group
                            group_name = str(row.get("group_name", "")).strip()
                            if not group_name or group_name == "null":
                                errors.append(f"Row {index + 2}: Group name is required")
                                error_count += 1
                                continue

                            # Parse associated_with (User) and get user instance
                            associated_with_email = str(row.get("associated_with", "")).strip()
                            if not associated_with_email or associated_with_email == "null":
                                errors.append(f"Row {index + 2}: Associated user is required")
                                error_count += 1
                                continue
                            try:
                                associated_with_user = User.objects.get(email=associated_with_email)
                            except User.DoesNotExist:
                                errors.append(
                                    f"Row {index + 2}: Associated user '{associated_with_email}' does not exist"
                                )
                                error_count += 1
                                continue

                            # Parse relationship
                            relationship = str(GuestGroup.RELATIONSHIP_CHOICES.RELATIVE)  # Default value as string
                            relationship_input = str(row.get("relationship", "")).strip()

                            if relationship_input:
                                # Check if input matches short code (case insensitive)
                                for choice_value, choice_label in GuestGroup.RELATIONSHIP_CHOICES.choices:
                                    if relationship_input.lower() == str(choice_value).lower():
                                        relationship = str(choice_value)
                                        break
                                    # Check if input matches long form (case insensitive)
                                    elif relationship_input.lower() == str(choice_label).lower():
                                        relationship = str(choice_value)
                                        break

                            # Parse priority
                            priority = row.get("priority")
                            if priority and str(priority).isdigit():
                                priority = int(priority)
                                if priority not in [choice[0] for choice in GuestGroup.PRIORITY_CHOICES.choices]:
                                    priority = GuestGroup.PRIORITY_CHOICES.MEDIUM
                            else:
                                priority = GuestGroup.PRIORITY_CHOICES.MEDIUM

                            guest_group, group_created = GuestGroup.objects.get_or_create(
                                name=group_name,
                                defaults={
                                    "created_by": request.user,
                                    "updated_by": request.user,
                                    "associated_with": associated_with_user,
                                    "email": str(row.get("group_email", "")).strip() if row.get("group_email") else "",
                                    "phone": str(row.get("group_phone", "")).strip() if row.get("group_phone") else "",
                                    "address": str(row.get("group_address", "")).strip()
                                    if row.get("group_address")
                                    else "",
                                    "city": str(row.get("group_city", "")).strip() if row.get("group_city") else "",
                                    "state": str(row.get("group_state", "")).strip() if row.get("group_state") else "",
                                    "zip_code": str(row.get("group_zip_code", "")).strip()
                                    if row.get("group_zip_code")
                                    else "",
                                    "relationship": relationship,
                                    "priority": priority,
                                    "notes": str(row.get("group_notes", "")).strip() if row.get("group_notes") else "",
                                },
                            )

                            # update existing group if not created
                            if not group_created:
                                guest_group.is_deleted = False
                                guest_group.associated_with = associated_with_user
                                guest_group.email = (
                                    str(row.get("group_email", "")).strip() if row.get("group_email") else ""
                                )
                                guest_group.phone = (
                                    str(row.get("group_phone", "")).strip() if row.get("group_phone") else ""
                                )
                                guest_group.address = (
                                    str(row.get("group_address", "")).strip() if row.get("group_address") else ""
                                )
                                guest_group.city = (
                                    str(row.get("group_city", "")).strip() if row.get("group_city") else ""
                                )
                                guest_group.state = (
                                    str(row.get("group_state", "")).strip() if row.get("group_state") else ""
                                )
                                guest_group.zip_code = (
                                    str(row.get("group_zip_code", "")).strip() if row.get("group_zip_code") else ""
                                )
                                guest_group.relationship = relationship
                                guest_group.priority = priority
                                guest_group.notes = (
                                    str(row.get("group_notes", "")).strip() if row.get("group_notes") else ""
                                )
                                guest_group.save()

                            # Validate guest names or plus_one status
                            first_name = str(row.get("first_name", "")).strip()
                            last_name = str(row.get("last_name", "")).strip()

                            # Parse plus_one status early for validation
                            plus_one = False
                            if row.get("plus_one") is not None:
                                plus_one_str = str(row.get("plus_one", "")).strip().lower()
                                plus_one = plus_one_str in ["true", "yes", "1", "y"]

                            # Validate that we have either names or plus_one=True
                            has_names = first_name and first_name != "null" and last_name and last_name != "null"

                            if not has_names and not plus_one:
                                errors.append(
                                    f"Row {index + 2}: Either 'first_name' and 'last_name' must be provided OR 'plus_one' must be True"
                                )
                                error_count += 1
                                continue

                            # For plus_one entries without names, generate placeholder names
                            if plus_one and not has_names:
                                first_name = guest_group.name
                                last_name = "Plus One"

                            # Parse remaining boolean fields
                            is_invited = False
                            if row.get("is_invited") is not None:
                                invited_str = str(row.get("is_invited", "")).strip().lower()
                                is_invited = invited_str in ["true", "yes", "1", "y"]

                            overnight = False
                            if row.get("overnight") is not None:
                                overnight_str = str(row.get("overnight", "")).strip().lower()
                                overnight = overnight_str in ["true", "yes", "1", "y"]

                            guest, guest_created = Guest.objects.get_or_create(
                                first_name=first_name,
                                last_name=last_name,
                                group=guest_group,
                                is_deleted=False,
                                defaults={
                                    "created_by": request.user,
                                    "updated_by": request.user,
                                    "plus_one": plus_one,
                                    "is_invited": is_invited,
                                    "overnight": overnight,
                                    "notes": str(row.get("guest_notes", "")).strip() if row.get("guest_notes") else "",
                                },
                            )

                            if guest_created:
                                success_count += 1
                            else:
                                # Update existing guest
                                guest.is_deleted = False
                                guest.plus_one = plus_one
                                guest.is_invited = is_invited
                                guest.overnight = overnight
                                guest.notes = (
                                    str(row.get("guest_notes", "")).strip() if row.get("guest_notes") else guest.notes
                                )
                                guest.response_notes = (
                                    str(row.get("response_notes", "")).strip()
                                    if row.get("response_notes")
                                    else guest.response_notes
                                )
                                guest.updated_by = request.user
                                guest.save()
                                update_count += 1

                        except Exception as e:
                            errors.append(f"Row {index + 2}: {str(e)}")
                            error_count += 1

                    # Show results
                    if success_count > 0:
                        messages.success(request, f"Successfully imported {success_count} guests.")

                    if update_count > 0:
                        messages.info(request, f"Updated {update_count} existing guests.")

                    if error_count > 0:
                        messages.warning(request, f"{error_count} guests had errors and were skipped.")
                        for error in errors[:5]:  # Show first 5 errors
                            messages.error(request, error)

                    if not success_count and not update_count and not error_count:
                        messages.info(request, "No guests found in the uploaded file.")

                except Exception as e:
                    messages.error(request, f"Error processing file: {str(e)}")

            else:
                messages.error(request, "Please select an Excel file to upload.")
                return redirect("guestlist:guestlist_summary")
        else:
            messages.error(request, "Invalid form submission. Please try again.")
        return redirect("guestlist:guestlist_summary")

    # Generate template file for download
    df = pl.DataFrame(
        data={
            "group_name": ["Smith Family", "Smith Family", "Johnson Family", "Work Colleagues"],
            "group_email": ["smith@email.com", "smith@email.com", "johnson@email.com", "colleagues@company.com"],
            "group_phone": ["555-0123", "555-0123", "555-0456", "555-0789"],
            "group_address": ["123 Main St", "123 Main St", "456 Oak Ave", "789 Business Blvd"],
            "group_city": ["Anytown", "Anytown", "Springfield", "Metro City"],
            "group_state": ["CA", "CA", "IL", "NY"],
            "group_zip_code": ["12345", "12345", "62701", "10001"],
            "relationship": ["Relative", "Relative", "Friend", "Colleague"],
            "priority": [3, 3, 2, 1],
            "associated_with": [
                "john.doe@email.com",
                "jane.smith@email.com",
                "john.doe@email.com",
                "jane.smith@email.com",
            ],
            "group_notes": ["Close family friends", "Close family friends", "College friends", "Work team"],
            "first_name": ["John", "Jane", "Bob", "Alice"],
            "last_name": ["Smith", "Smith", "Johnson", "Wilson"],
            "plus_one": ["FALSE", "FALSE", "TRUE", "FALSE"],
            "overnight": ["FALSE", "FALSE", "TRUE", "FALSE"],
            "is_invited": ["TRUE", "TRUE", "TRUE", "FALSE"],
            "guest_notes": ["Best man", "Maid of honor", "College roommate", "Project manager"],
        }
    )
    output = io.BytesIO()
    df.write_excel(output)
    output.seek(0)

    # Create the HTTP response with the Excel file
    response = HttpResponse(
        output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="guestlist_import_template.xlsx"'

    return response


@login_required
def guestlist_summary(request: HttpRequest) -> HttpResponse:
    """
    Displays the summary of guest groups and their guests.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template with guest group summary.
    """
    guest_groups = GuestGroup.objects.filter(is_deleted=False).prefetch_related("guests").order_by("-priority", "name")
    context = {
        "guest_groups": guest_groups,
        "form": GuestlistImportForm(),
        "delete_modal_url": reverse("guestlist:guest_group_delete_modal"),
        "total_guests": Guest.objects.filter(is_deleted=False).count(),
        "total_invited": Guest.objects.filter(is_deleted=False, is_invited=True).count(),
        "total_invited_standard": Guest.objects.filter(is_deleted=False, is_invited=True, vip=False).count(),
        "total_invited_vip": Guest.objects.filter(is_deleted=False, is_invited=True, vip=True).count(),
        "total_attending": Guest.objects.filter(is_deleted=False, is_attending=True).count(),
        "total_attending_standard": Guest.objects.filter(is_deleted=False, is_attending=True, overnight=False).count(),
        "total_attending_vip": Guest.objects.filter(is_deleted=False, is_attending=True, vip=True).count(),
        "total_attending_overnight": Guest.objects.filter(is_deleted=False, is_attending=True, overnight=True).count(),
        "total_declined": Guest.objects.filter(is_deleted=False, is_attending=False, responded=True).count(),
        "total_pending": Guest.objects.filter(is_deleted=False, responded=False, is_invited=True).count(),
    }
    return render(request, "guestlist/guestlist_summary.html", context)


@login_required
def all_guests(request: HttpRequest) -> HttpResponse:
    """
    Displays a table of all guests with their details.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template with all guests in a table format.
    """
    guests = (
        Guest.objects.filter(is_deleted=False)
        .select_related("group")
        .prefetch_related("group__associated_with")
        .order_by("last_name", "first_name")
    )

    context = {
        "block_title": "All Guests",
        "title": "All Guests",
        "guests": guests,
        "delete_modal_url": reverse("guestlist:guest_delete_modal"),
        "total_guests": Guest.objects.filter(is_deleted=False).count(),
        "total_invited": Guest.objects.filter(is_deleted=False, is_invited=True).count(),
        "total_invited_standard": Guest.objects.filter(is_deleted=False, is_invited=True, vip=False).count(),
        "total_invited_vip": Guest.objects.filter(is_deleted=False, is_invited=True, vip=True).count(),
        "total_attending": Guest.objects.filter(is_deleted=False, is_attending=True).count(),
        "total_attending_standard": Guest.objects.filter(is_deleted=False, is_attending=True, overnight=False).count(),
        "total_attending_vip": Guest.objects.filter(is_deleted=False, is_attending=True, vip=True).count(),
        "total_attending_overnight": Guest.objects.filter(is_deleted=False, is_attending=True, overnight=True).count(),
        "total_declined": Guest.objects.filter(is_deleted=False, is_attending=False, responded=True).count(),
        "total_pending": Guest.objects.filter(is_deleted=False, responded=False, is_invited=True).count(),
    }
    return render(request, "guestlist/guest_all.html", context)


@login_required
def guestgroup_detail(request: HttpRequest, group_slug: str) -> HttpResponse:
    """
    Displays the details of a specific guest group.

    Args:
        request (HttpRequest): The HTTP request object.
        group_slug (str): The slug of the guest group.

    Returns:
        HttpResponse: Rendered template with guest group details.
    """
    try:
        guest_group = GuestGroup.objects.get(slug=group_slug, is_deleted=False)
    except GuestGroup.DoesNotExist:
        messages.error(request, "Guest group not found.")
        return redirect("guestlist:guestlist_summary")

    breadcrumbs = [
        {"title": "Guest List", "url": reverse("guestlist:guestlist_summary")},
        {"title": f"{guest_group.name}", "url": None},
    ]
    attach_url_query = QueryDict("", mutable=True)
    attach_url_query["next"] = request.path
    context = {
        "block_title": f"{guest_group}",
        "breadcrumbs": breadcrumbs,
        "title": f"{guest_group}",
        "object": guest_group,
        "edit_url": reverse("guestlist:guestgroup_edit", args=[guest_group.slug]),
        "status": None,
        "status_text": None,
        "link_url": None,
        "image_url": None,
        "delete_modal_url": reverse("guestlist:guest_group_delete_modal"),
        "delete_child_modal_url": reverse("guestlist:guest_delete_modal"),
        "child_item_title": "Guests",
        "attachments": Attachment.objects.attachments_for_object(guest_group).all(),
        "attach_form": AttachmentUploadForm(),
        "attach_submit_url": str(
            reverse(
                "attachments:add_attachment",
                kwargs={"app_label": "guestlist", "model_name": "GuestGroup", "pk": guest_group.pk},
                query=attach_url_query,
            )
        ),
    }
    return render(request, "guestlist/guestgroup_detail.html", context)


@login_required
def guestgroup_create(request: HttpRequest) -> HttpResponse:
    """
    Creates a new guest group.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template with the guest group form for creation.
    """
    if request.method == "POST":
        form = GuestGroupForm(request.POST)
        if form.is_valid():
            guest_group = form.save(commit=False)
            guest_group.created_by = request.user
            guest_group.updated_by = request.user
            guest_group.save()
            messages.success(request, f"Guest group '{guest_group.name}' was created successfully.")
            return redirect("guestlist:guestgroup_detail", group_slug=guest_group.slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GuestGroupForm()

    intro = "Create a new guest group to organize your guests."
    breadcrumbs = [
        {"title": "Guest List", "url": reverse("guestlist:guestlist_summary")},
        {"title": "Create Guest Group", "url": None},
    ]
    context = {
        "block_title": "Create Guest Group",
        "breadcrumbs": breadcrumbs,
        "title": "Create Guest Group",
        "intro": intro,
        "form": form,
        "object": None,
        "submit_text": "Create Guest Group",
        "cancel_url": reverse("guestlist:guestlist_summary"),
        "first_field": "name",
    }
    return render(request, "form/object.html", context)


@login_required
def guestgroup_edit(request: HttpRequest, group_slug: str) -> HttpResponse:
    """
    Edits an existing guest group.

    Args:
        request (HttpRequest): The HTTP request object.
        group_slug (str): The slug of the guest group to edit.

    Returns:
        HttpResponse: Rendered template with the guest group form for editing.
    """
    guest_group = get_object_or_404(GuestGroup, slug=group_slug)

    if request.method == "POST":
        form = GuestGroupForm(request.POST, instance=guest_group)
        if form.is_valid():
            guest_group = form.save(commit=False)
            guest_group.updated_by = request.user
            guest_group.save()
            messages.success(request, f"Guest group '{guest_group.name}' was updated successfully.")
            return redirect("guestlist:guestgroup_detail", group_slug=guest_group.slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GuestGroupForm(instance=guest_group)

    intro = "Edit the details of the guest group."
    breadcrumbs = [
        {"title": "Guest List", "url": reverse("guestlist:guestlist_summary")},
        {"title": guest_group.name, "url": reverse("guestlist:guestgroup_detail", args=[guest_group.slug])},
        {"title": "Edit Guest Group", "url": None},
    ]
    context = {
        "block_title": "Edit Guest Group",
        "breadcrumbs": breadcrumbs,
        "title": f"Edit Guest Group: {guest_group}",
        "intro": intro,
        "form": form,
        "object": guest_group,
        "submit_text": "Update Guest Group",
        "cancel_url": reverse("guestlist:guestlist_summary"),
        "first_field": "name",
    }
    return render(request, "form/object.html", context)


@login_required
def guest_group_delete_modal(request: HttpRequest) -> HttpResponse | JsonResponse:
    guest_group_slug = request.GET.get("slug")
    if not guest_group_slug:
        return JsonResponse({"error": "Guest group slug is required"}, status=400)
    try:
        guest_group = GuestGroup.objects.get(slug=guest_group_slug, is_deleted=False)
    except GuestGroup.DoesNotExist:
        return JsonResponse({"error": "Guest group not found"}, status=404)

    context = {
        "object": guest_group,
        "object_type": "Guest Group",
        "action_url": reverse("guestlist:guest_group_delete", args=[guest_group.slug]),
    }
    return render(request, "components/modal/object_delete_modal_body.html", context)


@login_required
def guest_group_delete(request: HttpRequest, group_slug: str) -> HttpResponse:
    guest_group = get_object_or_404(GuestGroup, slug=group_slug)

    if request.method == "POST":
        # Soft delete the guest group and all its guests
        guest_group.is_deleted = True
        guest_group.updated_by = request.user
        guest_group.save()

        # Also soft delete all guests in this group
        for guest in guest_group.guests.all():
            guest.is_deleted = True
            guest.updated_by = request.user
            guest.save()

        messages.success(request, f"Guest group '{guest_group.name}' and all its guests have been deleted.")
        return redirect("guestlist:guestlist_summary")

    else:
        messages.error(request, "Invalid request method.")
        return redirect("guestlist:guestlist_summary")


@login_required
def guest_data(request: HttpRequest) -> HttpResponse | JsonResponse:
    """Fetch guest data for DataTables.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse | JsonResponse: The response containing guest data.
    """
    # optional filtering by group
    group_slug = request.GET.get("group")

    # Get DataTables parameters
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")

    # optional filtering by group
    group_slug = request.GET.get("group")

    # Get DataTables parameters
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")

    # Handle sorting
    order_column_index = request.GET.get("order[0][column]")
    order_direction = request.GET.get("order[0][dir]")
    order_column_name = request.GET.get(f"columns[{order_column_index}][name]")

    if group_slug:
        queryset = Guest.objects.filter(is_deleted=False, group__slug=group_slug).select_related("group")
    else:
        queryset = Guest.objects.filter(is_deleted=False)

    records_total = queryset.count()

    # Apply search filter if provided
    if search_value:
        queryset = queryset.filter(
            Q(first_name__icontains=search_value)
            | Q(last_name__icontains=search_value)
            | Q(group__name__icontains=search_value),
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

    data = []
    for guest in queryset:
        menu_content = render_to_string(
            "cotton/table/row_actions.html",
            {
                "detail_url": reverse("guestlist:guest_detail", args=[guest.slug]),
                "update_url": reverse("guestlist:guest_edit", args=[guest.slug]),
                "slug": guest.slug,
            },
        )

        if guest.is_invited:
            if guest.responded:
                attending_status = "Attending" if guest.is_attending else "Declined"
            else:
                attending_status = "Pending"
        else:
            attending_status = "Not Invited"

        if guest.group.associated_with:
            association = guest.group.associated_with.get_full_name()
        else:
            association = "Unknown"

        data.append(
            {
                "first_name": guest.first_name,
                "last_name": guest.last_name,
                "group": guest.group.name,
                "relationship": guest.group.get_relationship_display(),
                "plus_one": "Yes" if guest.plus_one else "No",
                "vip": "Yes" if guest.vip else "No",
                "overnight": "Yes" if guest.overnight else "No",
                "rsvp": attending_status,
                "association": association,
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
def guest_create(request: HttpRequest, group_slug: str | None = None) -> HttpResponse:
    """
    Creates a new guest.

    Args:
        request (HttpRequest): The HTTP request object.
        group_slug (str, optional): The slug of the guest group to associate the guest with.

    Returns:
        HttpResponse: Rendered template with the guest form for creation.
    """
    guest_group = None
    if group_slug:
        guest_group = get_object_or_404(GuestGroup, slug=group_slug)

    if request.method == "POST":
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.created_by = request.user
            guest.updated_by = request.user
            if guest_group:
                guest.group = guest_group
            guest.save()

            redirect_group = guest.group or guest_group
            if redirect_group:
                messages.success(request, f"Guest '{guest.first_name} {guest.last_name}' was created successfully.")
                return redirect("guestlist:guestgroup_detail", group_slug=redirect_group.slug)
            else:
                messages.success(request, f"Guest '{guest.first_name} {guest.last_name}' was created successfully.")
                return redirect("guestlist:guestlist_summary")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GuestForm()
        if guest_group:
            form.fields["group"].initial = guest_group

    intro = "Create a new guest"
    breadcrumbs = [
        {"title": "Guest List", "url": reverse("guestlist:guestlist_summary")},
        {"title": "Create Guest", "url": None},
    ]
    if guest_group:
        breadcrumbs.insert(
            1, {"title": guest_group.name, "url": reverse("guestlist:guestgroup_detail", args=[guest_group.slug])}
        )
        cancel_url = reverse("guestlist:guestgroup_detail", args=[guest_group.slug])
    else:
        cancel_url = reverse("guestlist:guestlist_summary")

    context = {
        "block_title": "Create Guest",
        "breadcrumbs": breadcrumbs,
        "title": "Create Guest",
        "intro": intro,
        "form": form,
        "object": None,
        "submit_text": "Create Guest",
        "cancel_url": cancel_url,
        "first_field": "name",
    }

    return render(request, "form/object.html", context)


@login_required
def guest_detail(request: HttpRequest, guest_slug: str) -> HttpResponse:
    """
    Displays the details of a specific guest.

    Args:
        request (HttpRequest): The HTTP request object.
        guest_slug (str): The slug of the guest.

    Returns:
        HttpResponse: Rendered template with guest details.
    """

    try:
        guest = Guest.objects.get(slug=guest_slug, is_deleted=False)
    except Guest.DoesNotExist:
        messages.error(request, "Guest not found.")
        return redirect("guestlist:guestlist_summary")

    breadcrumbs = [
        {"title": "Guest List", "url": reverse("guestlist:guestlist_summary")},
        {"title": guest.group, "url": reverse("guestlist:guestgroup_detail", args=[guest.group.slug])},
        {"title": guest, "url": None},
    ]
    attach_url_query = QueryDict("", mutable=True)
    attach_url_query["next"] = request.path
    context = {
        "block_title": f"{guest}",
        "breadcrumbs": breadcrumbs,
        "title": f"{guest}",
        "object": guest,
        "edit_url": reverse("guestlist:guest_edit", args=[guest.slug]),
        "status": guest.is_attending,
        "status_text": "Attending" if guest.is_attending else "Not Attending",
        "link_url": None,
        "image_url": None,
        "delete_modal_url": reverse("guestlist:guest_delete_modal"),
        "attachments": Attachment.objects.attachments_for_object(guest).all(),
        "attach_form": AttachmentUploadForm(),
        "attach_submit_url": str(
            reverse(
                "attachments:add_attachment",
                kwargs={"app_label": "guestlist", "model_name": "Guest", "pk": guest.pk},
                query=attach_url_query,
            )
        ),
    }
    return render(request, "guestlist/guest_detail.html", context)


@login_required
def guest_edit(request: HttpRequest, guest_slug: str) -> HttpResponse:
    """
    Edits an existing guest.

    Args:
        request (HttpRequest): The HTTP request object.
        guest_slug (str): The slug of the guest to edit.

    Returns:
        HttpResponse: Rendered template with the guest form for editing.
    """
    guest = get_object_or_404(Guest, slug=guest_slug)

    if request.method == "POST":
        form = GuestForm(request.POST, instance=guest)
        if form.is_valid():
            guest: Guest = form.save(commit=False)
            guest.updated_by = request.user
            guest.save()
            messages.success(request, f"Guest '{guest.first_name} {guest.last_name}' was updated successfully.")

            return redirect("guestlist:guest_detail", guest_slug=guest.slug)

    else:
        form = GuestForm(instance=guest)

    # configure rest of template context
    intro = f"Edit Guest: {guest.first_name} {guest.last_name}"
    breadcrumbs = [
        {"title": "Guest List", "url": reverse("guestlist:guestlist_summary")},
        {"title": guest.group, "url": reverse("guestlist:guestgroup_detail", args=[guest.group.slug])},
        {"title": guest, "url": None},
    ]
    cancel_url = reverse("guestlist:guest_detail", args=[guest.slug])

    context = {
        "block_title": "Edit Guest",
        "breadcrumbs": breadcrumbs,
        "title": f"Edit Guest: {guest.first_name} {guest.last_name}",
        "intro": intro,
        "form": form,
        "object": guest,
        "submit_text": "Save Changes",
        "cancel_url": cancel_url,
        "first_field": "name",
    }
    return render(request, "form/object.html", context)


@login_required
def guest_delete_modal(request: HttpRequest) -> HttpResponse:
    """Renders a modal confirmation dialog for deleting a guest.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered modal template for guest deletion confirmation.
    """

    guest_slug = request.GET.get("slug")
    if not guest_slug:
        return JsonResponse({"error": "Guest slug is required"}, status=400)
    try:
        guest = Guest.objects.get(slug=guest_slug, is_deleted=False)
    except Guest.DoesNotExist:
        return JsonResponse({"error": "Guest not found"}, status=404)

    context = {
        "object": guest,
        "object_type": "Guest",
        "action_url": reverse("guestlist:guest_delete", args=[guest.slug]),
    }
    return render(request, "components/modal/object_delete_modal_body.html", context)


@login_required
def guest_delete(request: HttpRequest, guest_slug: str) -> HttpResponse:
    """
    Deletes an existing guest (soft delete).

    Args:
        request (HttpRequest): The HTTP request object.
        guest_slug (str): The slug of the guest to delete.

    Returns:
        HttpResponse: Redirects to the appropriate page after deletion.
    """
    guest = get_object_or_404(Guest, slug=guest_slug)
    guest_group: GuestGroup = guest.group

    if request.method == "POST":
        # Soft delete the guest
        guest.is_deleted = True
        guest.updated_by = request.user
        guest.save()

        messages.success(request, f"Guest '{guest.first_name} {guest.last_name}' has been deleted.")

    else:
        messages.error(request, "Invalid request method.")

    # Redirect to group detail if guest belongs to a group, otherwise to summary
    if guest_group:
        return redirect("guestlist:guestgroup_detail", group_slug=guest_group.slug)
    else:
        return redirect("guestlist:guestlist_summary")


@login_required
def address_csv_export(request: HttpRequest) -> HttpResponse:
    """
    Exports the guest list to a CSV file formatted for use with an invitation service.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The CSV file response.
    """
    guest_groups = GuestGroup.objects.filter(is_deleted=False)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="guest_list.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Address", "Address2", "City", "State", "Zip", "Email"])
    for group in guest_groups:
        writer.writerow(
            [group.address_name, group.address, group.address_two, group.city, group.state, group.zip_code, group.email]
        )

    return response


def rsvp(request: HttpRequest) -> HttpResponse:
    """
    Render the 'RSVP' page of the application.
    """

    context: dict[str, Any] = {"guest_group": None}
    if request.method == "POST":
        # process submitted RSVP form
        rsvp_code = request.POST.get("rsvp_code")
        try:
            context["guest_group"] = GuestGroup.objects.get(rsvp_code=rsvp_code, is_deleted=False)
        except GuestGroup.DoesNotExist:
            messages.error(request, "Invalid RSVP code. Please try again.")
    else:
        rsvp_code = request.GET.get("code")
    if rsvp_code:
        try:
            context["guest_group"] = GuestGroup.objects.get(rsvp_code=rsvp_code.lstrip().rstrip(), is_deleted=False)
        except GuestGroup.DoesNotExist:
            messages.error(request, "Invalid RSVP code. Please try again.")

    context["form"] = RsvpCodeForm()
    context["submit_text"] = "Find My Invitation"
    context["cancel_url"] = reverse("core:home")

    return render(request, "guestlist/rsvp.html", context)


def rsvp_accept(request: HttpRequest, rsvp_code: str) -> HttpResponse:
    try:
        guest_group = GuestGroup.objects.get(rsvp_code=rsvp_code, is_deleted=False)
    except GuestGroup.DoesNotExist:
        messages.error(request, "Invalid RSVP code. Please try again.")
        return redirect("guestlist:rsvp")
    guests = guest_group.guests.filter(is_invited=True, is_deleted=False)

    if request.method == "POST":
        GuestRSVPFormSet = modelformset_factory(Guest, GuestRSVPForm, extra=0)
        guest_formset = GuestRSVPFormSet(request.POST, queryset=guests)
        submission_form = RsvpSubmissionForm(request.POST, prefix="rsvp_submission")

        if guest_formset.is_valid() and submission_form.is_valid():
            admin_user = User.objects.filter(is_admin=True).first()
            for form in guest_formset:
                guest: Guest = form.save(commit=False)
                guest.responded = True
                guest.updated_by = request.user if request.user.is_authenticated else admin_user
                guest.save()
            rsvp_submission = RsvpSubmission.objects.update_or_create(
                guest_group=guest_group,
                defaults={
                    "notes": submission_form.cleaned_data["notes"],
                    "email_updates": submission_form.cleaned_data.get("email_updates", False),
                    "email_address": submission_form.cleaned_data.get("email_address", ""),
                },
            )
            return redirect(f"{reverse('guestlist:rsvp_complete', args=[guest_group.rsvp_code])}?accepted=true")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        GuestRSVPFormSet = modelformset_factory(Guest, GuestRSVPForm, extra=0)
        guest_formset = GuestRSVPFormSet(queryset=guests)

        rsvp_submission, created = RsvpSubmission.objects.get_or_create(guest_group=guest_group)

    context = {
        "guest_group": guest_group,
        "guests": guests,
        "guest_formset": guest_formset,
        "rsvp_submission_form": RsvpSubmissionForm(prefix="rsvp_submission"),
        "show_accommodation": guests.filter(accommodation=True).exists(),
        "show_vip": guests.filter(vip=True).exists(),
    }

    return render(request, "guestlist/rsvp_accept.html", context)


def rsvp_complete(request: HttpRequest, rsvp_code: str) -> HttpResponse:
    """
    Render the 'RSVP Complete' page of the application.
    """
    try:
        guest_group = GuestGroup.objects.get(rsvp_code=rsvp_code, is_deleted=False)
    except GuestGroup.DoesNotExist:
        messages.error(request, "Invalid RSVP code. Please try again.")
        return redirect("guestlist:rsvp")

    if request.GET.get("accepted", "true").lower() == "true":
        accepted = True
    else:
        accepted = False
        # Mark all invited guests in the group as not attending
        invited_guests = guest_group.guests.filter(is_invited=True, is_deleted=False)
        admin_user = User.objects.filter(is_admin=True).first()
        for guest in invited_guests:
            guest.is_attending = False
            guest.responded = True
            guest.updated_by = request.user if request.user.is_authenticated else admin_user
            guest.save()

    context = {"accepted": accepted, "guest_group": guest_group}
    return render(request, "guestlist/rsvp_complete.html", context)
