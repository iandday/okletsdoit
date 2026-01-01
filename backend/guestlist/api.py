import logging
from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID, uuid4

from core.auth import multi_auth
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
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

router = Router(tags=["Guestlist"], auth=multi_auth)

logger = logging.getLogger(__name__)

User = get_user_model()


# Schemas
class GuestGroupSchema(Schema):
    id: UUID
    slug: str
    name: str
    address_name: str
    notes: str
    email: str
    phone: str
    address: str
    address_two: str
    city: str
    state: str
    zip_code: str
    relationship: str
    priority: int
    rsvp_code: str
    group_count: int
    group_standard: int
    group_vip: int
    group_overnight: int
    group_invited_count: int
    group_attending_count: int
    group_declined_count: int
    created_at: datetime
    updated_at: datetime


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
    notes: str
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

    for attr, value in payload.dict(exclude_unset=True).items():
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

    submission = RsvpSubmission.objects.create(guest_group_id=guest_group_id, **data)
    return submission


@router.put("/rsvp-submissions/{submission_id}", response=RsvpSubmissionSchema)
def update_rsvp_submission(request, submission_id: UUID, payload: RsvpSubmissionUpdateSchema):
    """Update an RSVP submission"""
    submission = get_object_or_404(RsvpSubmission, id=submission_id)

    for attr, value in payload.dict(exclude_unset=True).items():
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
