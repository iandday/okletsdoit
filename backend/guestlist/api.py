import csv
import logging
from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

from core.auth import multi_auth
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from import_export.formats import base_formats
from ninja import FilterSchema
from ninja import Query
from ninja import Router
from ninja import Schema
from ninja.errors import HttpError
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate

from .models import Guest
from .models import GuestGroup
from .models import RsvpQuestion
from .models import RsvpQuestionResponse
from .models import RsvpSubmission
from .resources import GuestGroupResource
from .resources import GuestResource

router = Router(tags=["Guestlist"], auth=multi_auth)

logger = logging.getLogger(__name__)

User = get_user_model()


# Schemas
class GuestGroupSchema(Schema):
    id: UUID
    slug: str
    name: str
    address_name: str
    notes: Optional[str] = None
    email: str
    phone: str
    address: str
    address_two: str
    city: str
    state: str
    zip_code: str
    relationship: str
    relationship_display: str
    priority: int
    priority_display: str
    associated_with_id: Optional[UUID] = None
    associated_with_first_name: Optional[str] = None
    associated_with_last_name: Optional[str] = None
    rsvp_code: str
    rsvp_url: str
    qr_code_url: Optional[str] = None
    has_qr_code: bool
    group_count: int
    group_standard: int
    group_vip: int
    group_overnight: int
    group_invited_count: int
    group_attending_count: int
    group_declined_count: int
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def resolve_rsvp_url(obj):
        from django.conf import settings

        return f"{settings.PERSONALIZED_RSVP_BASE_URL}/{obj.rsvp_code}"

    @staticmethod
    def resolve_qr_code_url(obj):
        if obj.qr_code:
            return f"/api/guestlist/guest-groups/{obj.id}/qr-code"
        return None

    @staticmethod
    def resolve_has_qr_code(obj):
        return obj.qr_code is not None

    @staticmethod
    def resolve_relationship_display(obj):
        return obj.get_relationship_display()

    @staticmethod
    def resolve_priority_display(obj):
        return obj.get_priority_display()

    @staticmethod
    def resolve_associated_with_first_name(obj):
        return obj.associated_with.first_name if obj.associated_with else None

    @staticmethod
    def resolve_associated_with_last_name(obj):
        return obj.associated_with.last_name if obj.associated_with else None


class GuestGroupFilterSchema(FilterSchema):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    relationship: Optional[str] = None
    priority: Optional[int] = None
    rsvp_code: Optional[str] = None


class GuestGroupCreateSchema(Schema):
    name: str
    address_name: Optional[str] = ""
    notes: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    address: Optional[str] = ""
    address_two: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    zip_code: Optional[str] = ""
    relationship: Optional[str] = "Rel"
    priority: Optional[int] = 2
    associated_with_id: Optional[UUID] = None


class GuestGroupUpdateSchema(Schema):
    name: Optional[str] = None
    address_name: Optional[str] = None
    notes: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    address_two: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    relationship: Optional[str] = None
    priority: Optional[int] = None
    associated_with_id: Optional[UUID] = None


class GuestSchema(Schema):
    id: UUID
    slug: str
    first_name: str
    last_name: str
    plus_one: bool
    group_id: Optional[UUID] = None
    is_invited: bool
    is_attending: bool
    responded: bool
    accept_accommodation: bool
    accept_vip: bool
    accommodation: bool
    vip: bool
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class GuestCreateSchema(Schema):
    first_name: str
    last_name: str
    plus_one: Optional[bool] = False
    group_id: Optional[UUID] = None
    is_invited: Optional[bool] = False
    is_attending: Optional[bool] = False
    responded: Optional[bool] = False
    accept_accommodation: Optional[bool] = False
    accept_vip: Optional[bool] = False
    accommodation: Optional[bool] = False
    vip: Optional[bool] = False
    notes: Optional[str] = ""


class GuestUpdateSchema(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    plus_one: Optional[bool] = None
    group_id: Optional[UUID] = None
    is_invited: Optional[bool] = None
    is_attending: Optional[bool] = None
    responded: Optional[bool] = None
    accept_accommodation: Optional[bool] = None
    accept_vip: Optional[bool] = None
    accommodation: Optional[bool] = None
    vip: Optional[bool] = None
    notes: Optional[str] = None


class RsvpSubmissionSchema(Schema):
    id: UUID
    guest_group_id: UUID
    email_updates: bool
    email_address: str
    notes: str
    accept_accommodation_count: int
    accept_vip_count: int
    created_at: datetime
    updated_at: datetime


class RsvpSubmissionFilterSchema(FilterSchema):
    rsvp_code: Optional[str] = None


class RsvpSubmissionCreateSchema(Schema):
    guest_group_id: UUID
    email_updates: Optional[bool] = False
    email_address: Optional[str] = ""
    notes: Optional[str] = ""


class RsvpSubmissionUpdateSchema(Schema):
    email_updates: Optional[bool] = None
    email_address: Optional[str] = None
    notes: Optional[str] = None


class ResponseChoiceSchema(Schema):
    id: UUID
    text: str


class RsvpQuestionResponseSchema(Schema):
    id: Optional[UUID] = None
    submission_id: Optional[UUID] = None
    question_id: UUID
    question_text: str
    question_type: str
    question_order: int
    response_text: Optional[str] = None
    response_choices: Optional[List[ResponseChoiceSchema]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RsvpQuestionResponseCreateSchema(Schema):
    submission_id: UUID
    question_id: UUID
    response_text: Optional[str] = None
    response_choice_ids: Optional[List[UUID]] = []


class RsvpQuestionResponseUpdateSchema(Schema):
    response_text: Optional[str] = None
    response_choice_ids: Optional[List[UUID]] = None


class RsvpDeclineResponseSchema(Schema):
    success: bool
    message: str


# GuestGroup CRUD Endpoints
@router.get("/guest-groups", response=List[GuestGroupSchema])
@paginate(PageNumberPagination, page_size=50)
def list_guest_groups(request, filters: GuestGroupFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all guest groups (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    return GuestGroup.objects.filter(q).order_by("-created_at")


@router.get("/guest-groups/{group_id}", response=GuestGroupSchema)
def get_guest_group(request, group_id: UUID):
    """Get a specific guest group by ID"""
    return get_object_or_404(GuestGroup, id=group_id, is_deleted=False)


@router.post("/guest-groups", response=GuestGroupSchema)
def create_guest_group(request, payload: GuestGroupCreateSchema):
    """Create a new guest group"""
    data = payload.dict()
    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user
    guest_group = GuestGroup.objects.create(**data)
    return guest_group


@router.put("/guest-groups/{group_id}", response=GuestGroupSchema)
def update_guest_group(request, group_id: UUID, payload: GuestGroupUpdateSchema):
    """Update a guest group"""
    guest_group = get_object_or_404(GuestGroup, id=group_id, is_deleted=False)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(guest_group, attr, value)

    if request.user.is_authenticated:
        guest_group.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            guest_group.updated_by = admin_user
    guest_group.save()
    return guest_group


@router.delete("/guest-groups/{group_id}")
def delete_guest_group(request, group_id: UUID):
    """Soft delete a guest group"""
    guest_group = get_object_or_404(GuestGroup, id=group_id, is_deleted=False)
    guest_group.is_deleted = True
    if request.user.is_authenticated:
        guest_group.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            guest_group.updated_by = admin_user
    guest_group.save()
    return {"success": True, "message": "Guest group deleted successfully"}


# Guest CRUD Endpoints
@router.get("/guests", response=List[GuestSchema])
@paginate(PageNumberPagination, page_size=50)
def list_guests(request, group_id: Optional[UUID] = None):
    """List all guests, optionally filtered by group"""
    queryset = Guest.objects.filter(is_deleted=False)
    if group_id:
        queryset = queryset.filter(group_id=group_id)
    return queryset.order_by("-created_at")


@router.get("/guests/{guest_id}", response=GuestSchema)
def get_guest(request, guest_id: UUID):
    """Get a specific guest by ID"""
    return get_object_or_404(Guest, id=guest_id, is_deleted=False)


@router.post("/guests", response=GuestSchema)
def create_guest(request, payload: GuestCreateSchema):
    """Create a new guest"""
    data = payload.dict()
    group_id = data.pop("group_id", None)

    # Validate group_id if provided
    if group_id is not None:
        _ = get_object_or_404(GuestGroup, id=group_id, is_deleted=False)

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user
    guest = Guest.objects.create(
        **data,
        group_id=group_id,
    )

    return guest


@router.put("/guests/{guest_id}", response=GuestSchema)
def update_guest(request, guest_id: UUID, payload: GuestUpdateSchema):
    """Update a guest"""
    guest = get_object_or_404(Guest, id=guest_id, is_deleted=False)

    data = payload.dict(exclude_unset=True)
    # Validate group_id if it's being changed
    if "group_id" in data:
        get_object_or_404(GuestGroup, id=data["group_id"], is_deleted=False)

    for attr, value in data.items():
        setattr(guest, attr, value)

    if request.user.is_authenticated:
        guest.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            guest.updated_by = admin_user
    guest.save()
    return guest


@router.delete("/guests/{guest_id}")
def delete_guest(request, guest_id: UUID):
    """Soft delete a guest"""
    guest = get_object_or_404(Guest, id=guest_id, is_deleted=False)
    guest.is_deleted = True
    if request.user.is_authenticated:
        guest.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            guest.updated_by = admin_user
    guest.save()
    return {"success": True, "message": "Guest deleted successfully"}


# RsvpSubmission CRUD Endpoints
@router.get("/rsvp-submissions", response=List[RsvpSubmissionSchema])
@paginate(PageNumberPagination, page_size=50)
def list_rsvp_submissions(request, filters: RsvpSubmissionFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all RSVP submissions"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    return RsvpSubmission.objects.filter(q).order_by("-created_at")


@router.get("/rsvp-submissions/{submission_id}", response=RsvpSubmissionSchema)
def get_rsvp_submission(request, submission_id: UUID):
    """Get a specific RSVP submission by ID"""
    return get_object_or_404(RsvpSubmission, id=submission_id)


@router.post("/rsvp-submissions", response=RsvpSubmissionSchema)
@transaction.atomic
def create_rsvp_submission(request, payload: RsvpSubmissionCreateSchema):
    """Create a new RSVP submission"""
    data = payload.dict()
    guest_group_id = data.pop("guest_group_id")

    # Validate that the guest_group exists
    get_object_or_404(GuestGroup, id=guest_group_id, is_deleted=False)

    submission = RsvpSubmission.objects.create(guest_group_id=guest_group_id, **data)
    return submission


@router.put("/rsvp-submissions/{submission_id}", response=RsvpSubmissionSchema)
def update_rsvp_submission(request, submission_id: UUID, payload: RsvpSubmissionUpdateSchema):
    """Update an RSVP submission"""
    submission = get_object_or_404(RsvpSubmission, id=submission_id)

    data = payload.dict(exclude_unset=True)
    # Validate guest_group_id if it's being changed
    if "guest_group_id" in data:
        get_object_or_404(GuestGroup, id=data["guest_group_id"], is_deleted=False)

    for attr, value in data.items():
        setattr(submission, attr, value)

    submission.save()
    return submission


@router.delete("/rsvp-submissions/{submission_id}")
def delete_rsvp_submission(request, submission_id: UUID):
    """Delete an RSVP submission"""
    submission = get_object_or_404(RsvpSubmission, id=submission_id)
    submission.delete()
    return {"success": True, "message": "RSVP submission deleted successfully"}


@router.post("/rsvp-decline/{rsvp_code}", response=RsvpDeclineResponseSchema)
def decline_rsvp(request, rsvp_code: str):
    """Decline an RSVP using the rsvp code"""
    try:
        guest_group = GuestGroup.objects.get(rsvp_code=rsvp_code, is_deleted=False)
    except GuestGroup.DoesNotExist:
        return {"success": False, "message": "Invalid RSVP code"}

    RsvpSubmission.objects.get_or_create(guest_group=guest_group)

    guests = Guest.objects.filter(group=guest_group, is_deleted=False)
    for guest in guests:
        guest.is_attending = False
        guest.responded = True
        guest.save()

    return {"success": True, "message": "RSVP declined successfully"}


@router.get("/rsvp-acceptance-questions/preview", response=List[RsvpQuestionResponseSchema])
def get_rsvp_acceptence_questions_preview(request):
    """Get RSVP acceptance questions for preview mode"""
    question_queryset = RsvpQuestion.objects.filter(is_deleted=False, published=True).order_by("order")

    # Build response with question details
    result = []
    for question in question_queryset:
        result.append(
            {
                "id": uuid4(),
                "submission_id": None,
                "question_id": question.id,
                "question_text": question.text,
                "question_type": question.question_type,
                "question_order": question.order,
                "response_text": None,
                "response_choices": [
                    {"id": choice.id, "text": choice.choice_text} for choice in question.choices.all()
                ],
                "created_at": None,
                "updated_at": None,
            }
        )
    return result


@router.get("/rsvp-acceptance-questions/{rsvp_code}", response=List[RsvpQuestionResponseSchema])
def get_rsvp_acceptance_questions(request, rsvp_code: str):
    """Get or create RSVP acceptance questions for a guest group"""
    try:
        guest_group = GuestGroup.objects.get(rsvp_code=rsvp_code, is_deleted=False)
    except GuestGroup.DoesNotExist:
        raise HttpError(404, "Invalid RSVP code")

    rsvp_submission, created = RsvpSubmission.objects.get_or_create(guest_group=guest_group)
    for question in RsvpQuestion.objects.filter(is_deleted=False, published=True).order_by("order"):
        RsvpQuestionResponse.objects.update_or_create(
            submission=rsvp_submission,
            question=question,
        )
    question_queryset = (
        RsvpQuestionResponse.objects.filter(submission=rsvp_submission, question__published=True)
        .select_related("question")
        .prefetch_related("response_choices")
        .order_by("question__order")
    )

    # Build response with question details
    result = []
    for response in question_queryset:
        # Get response choices with id and text
        response_choices = [{"id": choice.id, "text": choice.choice_text} for choice in response.response_choices.all()]

        result.append(
            {
                "id": response.id,
                "submission_id": response.submission.id,
                "question_id": response.question.id,
                "question_text": response.question.text,
                "question_type": response.question.question_type,
                "question_order": response.question.order,
                "response_text": response.response_text,
                "response_choices": response_choices,
                "created_at": response.created_at,
                "updated_at": response.updated_at,
            }
        )
    return result


# RsvpQuestionResponse CRUD Endpoints
@router.get("/rsvp-responses", response=List[RsvpQuestionResponseSchema])
@paginate(PageNumberPagination, page_size=50)
def list_rsvp_responses(request, submission_id: Optional[UUID] = None):
    """List all RSVP question responses, optionally filtered by submission"""
    queryset = RsvpQuestionResponse.objects.filter(is_deleted=False)
    if submission_id:
        queryset = queryset.filter(submission_id=submission_id)
    return queryset.order_by("-created_at")


@router.get("/rsvp-responses/{response_id}", response=RsvpQuestionResponseSchema)
def get_rsvp_response(request, response_id: UUID):
    """Get a specific RSVP question response by ID"""
    rsvp_response = get_object_or_404(RsvpQuestionResponse, id=response_id, is_deleted=False)
    response_choices = [
        {"id": choice.id, "text": choice.choice_text} for choice in rsvp_response.response_choices.all()
    ]
    return {
        "id": rsvp_response.id,
        "submission_id": rsvp_response.submission.id,
        "question_id": rsvp_response.question.id,
        "question_text": rsvp_response.question.text,
        "question_type": rsvp_response.question.question_type,
        "question_order": rsvp_response.question.order,
        "response_text": rsvp_response.response_text,
        "response_choices": response_choices,
        "created_at": rsvp_response.created_at,
        "updated_at": rsvp_response.updated_at,
    }


@router.post("/rsvp-responses", response=RsvpQuestionResponseSchema)
@transaction.atomic
def create_rsvp_response(request, payload: RsvpQuestionResponseCreateSchema):
    """Create a new RSVP question response"""
    data = payload.dict()
    choice_ids = data.pop("response_choice_ids", [])

    # Validate that the submission and question exist
    get_object_or_404(RsvpSubmission, id=data["submission_id"], is_deleted=False)
    get_object_or_404(RsvpQuestion, id=data["question_id"], is_deleted=False)

    rsvp_response = RsvpQuestionResponse.objects.create(
        submission_id=data["submission_id"],
        question_id=data["question_id"],
        response_text=data.get("response_text"),
    )

    if choice_ids:
        rsvp_response.response_choices.set(choice_ids)

    response_choices = [
        {"id": choice.id, "text": choice.choice_text} for choice in rsvp_response.response_choices.all()
    ]
    return {
        "id": rsvp_response.id,
        "submission_id": rsvp_response.submission.id,
        "question_id": rsvp_response.question.id,
        "question_text": rsvp_response.question.text,
        "question_type": rsvp_response.question.question_type,
        "question_order": rsvp_response.question.order,
        "response_text": rsvp_response.response_text,
        "response_choices": response_choices,
        "created_at": rsvp_response.created_at,
        "updated_at": rsvp_response.updated_at,
    }


@router.put("/rsvp-responses/{response_id}", response=RsvpQuestionResponseSchema)
@transaction.atomic
def update_rsvp_response(request, response_id: UUID, payload: RsvpQuestionResponseUpdateSchema):
    """Update an RSVP question response"""
    rsvp_response = get_object_or_404(RsvpQuestionResponse, id=response_id, is_deleted=False)

    data = payload.dict(exclude_unset=True)
    logger.info(f"Updating response {response_id} with data: {data}")
    choice_ids = data.pop("response_choice_ids", None)

    for attr, value in data.items():
        setattr(rsvp_response, attr, value)

    if choice_ids is not None:
        rsvp_response.response_choices.set(choice_ids)

    rsvp_response.save()

    response_choices = [
        {"id": choice.id, "text": choice.choice_text} for choice in rsvp_response.response_choices.all()
    ]
    return {
        "id": rsvp_response.id,
        "submission_id": rsvp_response.submission.id,
        "question_id": rsvp_response.question.id,
        "question_text": rsvp_response.question.text,
        "question_type": rsvp_response.question.question_type,
        "question_order": rsvp_response.question.order,
        "response_text": rsvp_response.response_text,
        "response_choices": response_choices,
        "created_at": rsvp_response.created_at,
        "updated_at": rsvp_response.updated_at,
    }


@router.delete("/rsvp-responses/{response_id}")
def delete_rsvp_response(request, response_id: UUID):
    """Soft delete an RSVP question response"""
    response = get_object_or_404(RsvpQuestionResponse, id=response_id, is_deleted=False)
    response.is_deleted = True
    response.save()
    return {"success": True, "message": "RSVP response deleted successfully"}


@router.get("/export_address_csv")
def export_address_csv(request):
    guest_groups = GuestGroup.objects.filter(is_deleted=False)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="guest_addresses.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Address", "Address2", "City", "State", "Zip", "Email", "RSVP Code"])

    for group in guest_groups:
        writer.writerow(
            [
                group.address_name,
                group.address,
                group.address_two,
                group.city,
                group.state,
                group.zip_code,
                group.email,
                group.rsvp_code,
            ]
        )

    return response


@router.get(
    "/export_guest_data",
    response=None,
    openapi_extra={
        "responses": {
            200: {
                "description": "File download (CSV or Excel)",
                "content": {
                    "text/csv": {"schema": {"type": "string", "format": "binary"}},
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
                        "schema": {"type": "string", "format": "binary"}
                    },
                },
            }
        }
    },
)
def export_guest_data(request, format: str = "csv", fields: Optional[str] = None):
    """
    Export guest data as CSV or Excel file using django-import-export.

    Query parameters:
    - format: 'csv' or 'xlsx' (default: 'csv')
    - fields: Comma-separated list of field names to include (default: all fields)

    Available fields are dynamically derived from GuestResource.
    """

    # Validate format
    format_lower = format.lower()
    if format_lower == "excel":
        format_lower = "xlsx"

    if format_lower not in ["csv", "xlsx"]:
        raise HttpError(400, "Invalid format. Use 'csv' or 'excel'")

    # Get the resource and queryset
    resource = GuestResource()
    queryset = resource.get_queryset()

    # Get all available fields from resource
    available_fields = list(resource.fields.keys())

    # Parse and validate requested fields
    if fields:
        requested_fields = [f.strip() for f in fields.split(",")]
        selected_fields = [f for f in requested_fields if f in available_fields]
        if not selected_fields:
            raise HttpError(400, "No valid fields specified")
    else:
        selected_fields = available_fields

    # Preserve original export order, but filter to selected fields
    original_order = list(GuestResource.Meta.export_order)
    filtered_order = [f for f in original_order if f in selected_fields]

    # Create a custom resource with only selected fields
    class CustomGuestResource(GuestResource):
        class Meta(GuestResource.Meta):
            fields = selected_fields
            export_order = filtered_order

    custom_resource = CustomGuestResource()

    # Get the appropriate format
    export_data = custom_resource.export(queryset, request=request)

    if format_lower == "csv":
        format_instance = base_formats.CSV()
        csv_data = format_instance.export_data(export_data)
        response = HttpResponse(csv_data, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="guest_data.csv"'
    else:  # xlsx
        format_instance = base_formats.XLSX()
        xlsx_bytes = format_instance.export_data(export_data)
        response = HttpResponse(
            xlsx_bytes, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="guest_data.xlsx"'

    return response


@router.get(
    "/export_guest_group_data",
    response=None,
    openapi_extra={
        "responses": {
            200: {
                "description": "File download (CSV or Excel)",
                "content": {
                    "text/csv": {"schema": {"type": "string", "format": "binary"}},
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
                        "schema": {"type": "string", "format": "binary"}
                    },
                },
            }
        }
    },
)
def export_guest_group_data(request, format: str = "csv", fields: Optional[str] = None):
    """
    Export guest group data as CSV or Excel file using django-import-export.

    Query parameters:
    - format: 'csv' or 'xlsx' (default: 'csv')
    - fields: Comma-separated list of field names to include (default: all fields)

    Available fields are dynamically derived from GuestGroupResource.
    """
    # Validate format
    format_lower = format.lower()
    if format_lower == "excel":
        format_lower = "xlsx"

    if format_lower not in ["csv", "xlsx"]:
        raise HttpError(400, "Invalid format. Use 'csv' or 'excel'")

    # Get the resource and queryset
    resource = GuestGroupResource()
    queryset = resource.get_queryset()

    # Get all available fields from resource
    available_fields = list(resource.fields.keys())

    # Parse and validate requested fields
    if fields:
        requested_fields = [f.strip() for f in fields.split(",")]
        selected_fields = [f for f in requested_fields if f in available_fields]
        if not selected_fields:
            raise HttpError(400, "No valid fields specified")
    else:
        selected_fields = available_fields

    # Preserve original export order, but filter to selected fields
    original_order = list(GuestGroupResource.Meta.export_order)
    filtered_order = [f for f in original_order if f in selected_fields]

    # Create a custom resource with only selected fields
    class CustomGuestGroupResource(GuestGroupResource):
        class Meta(GuestGroupResource.Meta):
            fields = selected_fields
            export_order = filtered_order

    custom_resource = CustomGuestGroupResource()

    # Get the appropriate format
    export_data = custom_resource.export(queryset, request=request)

    if format_lower == "csv":
        format_instance = base_formats.CSV()
        csv_data = format_instance.export_data(export_data)
        response = HttpResponse(csv_data, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="guest_group_data.csv"'
    else:  # xlsx
        format_instance = base_formats.XLSX()
        xlsx_bytes = format_instance.export_data(export_data)
        response = HttpResponse(
            xlsx_bytes, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="guest_group_data.xlsx"'

    return response


@router.get("/guest-groups/{group_id}/qr-code")
def get_guest_group_qr_code(request, group_id: UUID):
    """Get QR code image for a guest group"""
    from django.http import FileResponse
    from django.http import HttpResponse

    guest_group = get_object_or_404(GuestGroup, id=group_id, is_deleted=False)

    if not guest_group.qr_code:
        return HttpResponse("QR code not available", status=404)

    # Return the image file directly
    try:
        return FileResponse(
            guest_group.qr_code.attachment_file.open("rb"),
            content_type="image/png",
            as_attachment=False,
            filename=f"qr_code_{guest_group.rsvp_code}.png",
        )
    except Exception as e:
        logger.error(f"Error retrieving QR code for guest group {group_id}: {e}")
        return HttpResponse("Error retrieving QR code", status=500)


class QRCodeTaskSchema(Schema):
    success: bool
    message: str
    task_id: str


@router.post("/qr-codes/generate-missing", response=QRCodeTaskSchema)
def generate_missing_qr_codes(request):
    """Trigger a Celery task to generate QR codes for guest groups that don't have one"""
    from guestlist.tasks import generate_missing_qr_codes as generate_task

    task = generate_task.delay()

    return {
        "success": True,
        "message": "QR code generation task started",
        "task_id": task.id,
    }


@router.post("/qr-codes/regenerate-all", response=QRCodeTaskSchema)
def regenerate_all_qr_codes(request):
    """Trigger a Celery task to regenerate ALL QR codes for guest groups"""
    from guestlist.tasks import regenerate_all_qr_codes as regenerate_task

    task = regenerate_task.delay()

    return {
        "success": True,
        "message": "QR code regeneration task started",
        "task_id": task.id,
    }
