import io
import logging
import polars as pl
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .forms import GuestlistImportForm, GuestGroupForm, GuestForm
from .models import GuestGroup, Guest
from users.models import User

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

                            is_attending = False
                            if row.get("is_attending") is not None:
                                attending_str = str(row.get("is_attending", "")).strip().lower()
                                is_attending = attending_str in ["true", "yes", "1", "y"]

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
        "total_guests": Guest.objects.filter(is_deleted=False).count(),
        "total_invited": Guest.objects.filter(is_deleted=False, is_invited=True).count(),
        "total_invited_day": Guest.objects.filter(is_deleted=False, is_invited=True, overnight=False).count(),
        "total_invited_overnight": Guest.objects.filter(is_deleted=False, is_invited=True, overnight=True).count(),
        "total_attending": Guest.objects.filter(is_deleted=False, is_attending=True).count(),
        "total_attending_day": Guest.objects.filter(is_deleted=False, is_attending=True, overnight=False).count(),
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
        "guests": guests,
        "total_guests": Guest.objects.filter(is_deleted=False).count(),
        "total_invited": Guest.objects.filter(is_deleted=False, is_invited=True).count(),
        "total_invited_day": Guest.objects.filter(is_deleted=False, is_invited=True, overnight=False).count(),
        "total_invited_overnight": Guest.objects.filter(is_deleted=False, is_invited=True, overnight=True).count(),
        "total_attending": Guest.objects.filter(is_deleted=False, is_attending=True).count(),
        "total_attending_day": Guest.objects.filter(is_deleted=False, is_attending=True, overnight=False).count(),
        "total_attending_overnight": Guest.objects.filter(is_deleted=False, is_attending=True, overnight=True).count(),
        "total_declined": Guest.objects.filter(is_deleted=False, is_attending=False, responded=True).count(),
        "total_pending": Guest.objects.filter(is_deleted=False, responded=False, is_invited=True).count(),
    }
    return render(request, "guestlist/all_guests.html", context)


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
    guest_group = get_object_or_404(GuestGroup, slug=group_slug)
    context = {
        "guest_group": guest_group,
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

    context = {
        "form": form,
        "title": "Create Guest Group",
        "submit_text": "Create Group",
        "is_edit": False,
    }
    return render(request, "guestlist/guestgroup_form.html", context)


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

    context = {
        "form": form,
        "guest_group": guest_group,
        "title": f"Edit {guest_group.name}",
        "submit_text": "Update Group",
        "is_edit": True,
    }
    return render(request, "guestlist/guestgroup_form.html", context)


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

    context = {
        "form": form,
        "guest_group": guest_group,
        "title": "Add Guest" + (f" to {guest_group.name}" if guest_group else ""),
        "submit_text": "Add Guest",
        "is_edit": False,
    }
    return render(request, "guestlist/guest_form.html", context)


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
            guest = form.save(commit=False)
            guest.updated_by = request.user
            guest.save()

            if guest.group:
                messages.success(request, f"Guest '{guest.first_name} {guest.last_name}' was updated successfully.")
                return redirect("guestlist:guestgroup_detail", group_slug=guest.group.slug)
            else:
                messages.success(request, f"Guest '{guest.first_name} {guest.last_name}' was updated successfully.")
                return redirect("guestlist:guestlist_summary")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GuestForm(instance=guest)

    context = {
        "form": form,
        "guest": guest,
        "guest_group": guest.group,
        "title": f"Edit {guest.first_name} {guest.last_name}",
        "submit_text": "Update Guest",
        "is_edit": True,
    }
    return render(request, "guestlist/guest_form.html", context)


@login_required
def guestgroup_delete(request: HttpRequest, group_slug: str) -> HttpResponse:
    """
    Deletes an existing guest group (soft delete).

    Args:
        request (HttpRequest): The HTTP request object.
        group_slug (str): The slug of the guest group to delete.

    Returns:
        HttpResponse: Redirects to the guest list summary page.
    """
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

    # For GET requests, show a confirmation page
    context = {
        "guest_group": guest_group,
        "guest_count": guest_group.guests.count(),
    }
    return render(request, "guestlist/guestgroup_confirm_delete.html", context)


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
    guest = get_object_or_404(Guest, slug=guest_slug)
    context = {
        "guest": guest,
    }
    return render(request, "guestlist/guest_detail.html", context)


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
    guest_group = guest.group

    if request.method == "POST":
        # Soft delete the guest
        guest.is_deleted = True
        guest.updated_by = request.user
        guest.save()

        messages.success(request, f"Guest '{guest.first_name} {guest.last_name}' has been deleted.")

        # Redirect to group detail if guest belongs to a group, otherwise to summary
        if guest_group:
            return redirect("guestlist:guestgroup_detail", group_slug=guest_group.slug)
        else:
            return redirect("guestlist:guestlist_summary")

    # For GET requests, show a confirmation page
    context = {
        "guest": guest,
        "guest_group": guest_group,
    }
    return render(request, "guestlist/guest_confirm_delete.html", context)
