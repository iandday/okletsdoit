from datetime import date
from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import FilterSchema
from ninja import Query
from ninja import Router
from ninja import Schema
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate

from core.auth import multi_auth

from .models import Deadline
from .models import DeadlineList

User = get_user_model()

router = Router(tags=["Deadlines"], auth=multi_auth)


# Schemas
class DeadlineListSchema(Schema):
    id: UUID
    name: str
    slug: Optional[str] = None
    count: int
    completed_count: int
    pending_count: int
    completion_percentage: float
    created_by_id: Optional[UUID] = None
    created_by_name: Optional[str] = None
    updated_by_id: Optional[UUID] = None
    updated_by_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class DeadlineListCreateSchema(Schema):
    name: str


class DeadlineListUpdateSchema(Schema):
    name: Optional[str] = None


class DeadlineSchema(Schema):
    id: UUID
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    deadline_list_id: Optional[UUID] = None
    deadline_list_name: Optional[str] = None
    due_date: Optional[date] = None
    assigned_to_id: Optional[UUID] = None
    assigned_to_name: Optional[str] = None
    completed: bool
    completed_at: Optional[datetime] = None
    completed_note: Optional[str] = None
    overdue: bool
    created_by_id: Optional[UUID] = None
    created_by_name: Optional[str] = None
    updated_by_id: Optional[UUID] = None
    updated_by_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class DeadlineFilterSchema(FilterSchema):
    deadline_list_id: Optional[UUID] = None
    completed: Optional[bool] = None
    assigned_to_id: Optional[UUID] = None


class DeadlineCreateSchema(Schema):
    name: str
    description: Optional[str] = None
    deadline_list_id: Optional[UUID] = None
    due_date: Optional[date] = None
    assigned_to_id: Optional[UUID] = None
    completed: Optional[bool] = False
    completed_note: Optional[str] = None


class DeadlineUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    deadline_list_id: Optional[UUID] = None
    due_date: Optional[date] = None
    assigned_to_id: Optional[UUID] = None
    completed: Optional[bool] = None
    completed_note: Optional[str] = None


# DeadlineList CRUD Endpoints
@router.get("/deadline-lists", response=List[DeadlineListSchema])
@paginate(PageNumberPagination, page_size=50)
def list_deadline_lists(request):
    """List all deadline lists (non-deleted)"""
    deadline_lists = DeadlineList.objects.filter(is_deleted=False).order_by("name")

    return [
        {
            "id": dl.id,
            "name": dl.name,
            "slug": dl.slug,
            "count": dl.count,
            "completed_count": dl.completed_count,
            "pending_count": dl.pending_count,
            "completion_percentage": dl.completion_percentage,
            "created_by_id": dl.created_by.id if dl.created_by else None,
            "created_by_name": dl.created_by.get_full_name() if dl.created_by else None,
            "updated_by_id": dl.updated_by.id if dl.updated_by else None,
            "updated_by_name": dl.updated_by.get_full_name() if dl.updated_by else None,
            "created_at": dl.created_at,
            "updated_at": dl.updated_at,
        }
        for dl in deadline_lists
    ]


@router.get("/deadline-lists/{list_id}", response=DeadlineListSchema)
def get_deadline_list(request, list_id: UUID):
    """Get a specific deadline list by ID"""
    dl = get_object_or_404(DeadlineList, id=list_id, is_deleted=False)
    return {
        "id": dl.id,
        "name": dl.name,
        "slug": dl.slug,
        "count": dl.count,
        "completed_count": dl.completed_count,
        "pending_count": dl.pending_count,
        "completion_percentage": dl.completion_percentage,
        "created_by_id": dl.created_by.id if dl.created_by else None,
        "created_by_name": dl.created_by.get_full_name() if dl.created_by else None,
        "updated_by_id": dl.updated_by.id if dl.updated_by else None,
        "updated_by_name": dl.updated_by.get_full_name() if dl.updated_by else None,
        "created_at": dl.created_at,
        "updated_at": dl.updated_at,
    }


@router.post("/deadline-lists", response=DeadlineListSchema)
def create_deadline_list(request, payload: DeadlineListCreateSchema):
    """Create a new deadline list"""
    data = payload.dict()

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    deadline_list = DeadlineList.objects.create(**data)

    return {
        "id": deadline_list.id,
        "name": deadline_list.name,
        "slug": deadline_list.slug,
        "count": deadline_list.count,
        "completed_count": deadline_list.completed_count,
        "pending_count": deadline_list.pending_count,
        "completion_percentage": deadline_list.completion_percentage,
        "created_by_id": deadline_list.created_by.id if deadline_list.created_by else None,
        "created_by_name": deadline_list.created_by.get_full_name() if deadline_list.created_by else None,
        "updated_by_id": deadline_list.updated_by.id if deadline_list.updated_by else None,
        "updated_by_name": deadline_list.updated_by.get_full_name() if deadline_list.updated_by else None,
        "created_at": deadline_list.created_at,
        "updated_at": deadline_list.updated_at,
    }


@router.put("/deadline-lists/{list_id}", response=DeadlineListSchema)
def update_deadline_list(request, list_id: UUID, payload: DeadlineListUpdateSchema):
    """Update a deadline list"""
    deadline_list = get_object_or_404(DeadlineList, id=list_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)

    for attr, value in data.items():
        setattr(deadline_list, attr, value)

    if request.user.is_authenticated:
        deadline_list.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            deadline_list.updated_by = admin_user

    deadline_list.save()

    return {
        "id": deadline_list.id,
        "name": deadline_list.name,
        "slug": deadline_list.slug,
        "count": deadline_list.count,
        "completed_count": deadline_list.completed_count,
        "pending_count": deadline_list.pending_count,
        "completion_percentage": deadline_list.completion_percentage,
        "created_by_id": deadline_list.created_by.id if deadline_list.created_by else None,
        "created_by_name": deadline_list.created_by.get_full_name() if deadline_list.created_by else None,
        "updated_by_id": deadline_list.updated_by.id if deadline_list.updated_by else None,
        "updated_by_name": deadline_list.updated_by.get_full_name() if deadline_list.updated_by else None,
        "created_at": deadline_list.created_at,
        "updated_at": deadline_list.updated_at,
    }


@router.delete("/deadline-lists/{list_id}")
def delete_deadline_list(request, list_id: UUID):
    """Soft delete a deadline list"""
    deadline_list = get_object_or_404(DeadlineList, id=list_id, is_deleted=False)
    deadline_list.is_deleted = True
    if request.user.is_authenticated:
        deadline_list.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            deadline_list.updated_by = admin_user
    deadline_list.save()
    return {"success": True, "message": "Deadline list deleted successfully"}


# Deadline CRUD Endpoints
@router.get("/deadlines", response=List[DeadlineSchema])
@paginate(PageNumberPagination, page_size=50)
def list_deadlines(request, filters: DeadlineFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all deadlines (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    deadlines = (
        Deadline.objects.filter(q).select_related("deadline_list", "assigned_to").order_by("due_date", "created_at")
    )

    return [
        {
            "id": deadline.id,
            "name": deadline.name,
            "slug": deadline.slug,
            "description": deadline.description,
            "deadline_list_id": deadline.deadline_list.id if deadline.deadline_list else None,
            "deadline_list_name": deadline.deadline_list.name if deadline.deadline_list else None,
            "due_date": deadline.due_date,
            "assigned_to_id": deadline.assigned_to.id if deadline.assigned_to else None,
            "assigned_to_name": deadline.assigned_to.get_full_name() if deadline.assigned_to else None,
            "completed": deadline.completed,
            "completed_at": deadline.completed_at,
            "completed_note": deadline.completed_note,
            "overdue": deadline.overdue_status(),
            "created_by_id": deadline.created_by.id if deadline.created_by else None,
            "created_by_name": deadline.created_by.get_full_name() if deadline.created_by else None,
            "updated_by_id": deadline.updated_by.id if deadline.updated_by else None,
            "updated_by_name": deadline.updated_by.get_full_name() if deadline.updated_by else None,
            "created_at": deadline.created_at,
            "updated_at": deadline.updated_at,
        }
        for deadline in deadlines
    ]


@router.get("/deadlines/{deadline_id}", response=DeadlineSchema)
def get_deadline(request, deadline_id: UUID):
    """Get a specific deadline by ID"""
    deadline = get_object_or_404(Deadline, id=deadline_id, is_deleted=False)
    return {
        "id": deadline.id,
        "name": deadline.name,
        "slug": deadline.slug,
        "description": deadline.description,
        "deadline_list_id": deadline.deadline_list.id if deadline.deadline_list else None,
        "deadline_list_name": deadline.deadline_list.name if deadline.deadline_list else None,
        "due_date": deadline.due_date,
        "assigned_to_id": deadline.assigned_to.id if deadline.assigned_to else None,
        "assigned_to_name": deadline.assigned_to.get_full_name() if deadline.assigned_to else None,
        "completed": deadline.completed,
        "completed_at": deadline.completed_at,
        "completed_note": deadline.completed_note,
        "overdue": deadline.overdue_status(),
        "created_by_id": deadline.created_by.id if deadline.created_by else None,
        "created_by_name": deadline.created_by.get_full_name() if deadline.created_by else None,
        "updated_by_id": deadline.updated_by.id if deadline.updated_by else None,
        "updated_by_name": deadline.updated_by.get_full_name() if deadline.updated_by else None,
        "created_at": deadline.created_at,
        "updated_at": deadline.updated_at,
    }


@router.post("/deadlines", response=DeadlineSchema)
def create_deadline(request, payload: DeadlineCreateSchema):
    """Create a new deadline"""
    data = payload.dict()
    deadline_list_id = data.pop("deadline_list_id", None)
    assigned_to_id = data.pop("assigned_to_id", None)

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    if deadline_list_id:
        deadline_list = get_object_or_404(DeadlineList, id=deadline_list_id, is_deleted=False)
        data["deadline_list"] = deadline_list

    if assigned_to_id:
        assigned_to = get_object_or_404(User, id=assigned_to_id)
        data["assigned_to"] = assigned_to

    deadline = Deadline.objects.create(**data)

    return {
        "id": deadline.id,
        "name": deadline.name,
        "slug": deadline.slug,
        "description": deadline.description,
        "deadline_list_id": deadline.deadline_list.id if deadline.deadline_list else None,
        "deadline_list_name": deadline.deadline_list.name if deadline.deadline_list else None,
        "due_date": deadline.due_date,
        "assigned_to_id": deadline.assigned_to.id if deadline.assigned_to else None,
        "assigned_to_name": deadline.assigned_to.get_full_name() if deadline.assigned_to else None,
        "completed": deadline.completed,
        "completed_at": deadline.completed_at,
        "completed_note": deadline.completed_note,
        "overdue": deadline.overdue_status(),
        "created_by_id": deadline.created_by.id if deadline.created_by else None,
        "created_by_name": deadline.created_by.get_full_name() if deadline.created_by else None,
        "updated_by_id": deadline.updated_by.id if deadline.updated_by else None,
        "updated_by_name": deadline.updated_by.get_full_name() if deadline.updated_by else None,
        "created_at": deadline.created_at,
        "updated_at": deadline.updated_at,
    }


@router.put("/deadlines/{deadline_id}", response=DeadlineSchema)
def update_deadline(request, deadline_id: UUID, payload: DeadlineUpdateSchema):
    """Update a deadline"""
    deadline = get_object_or_404(Deadline, id=deadline_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)
    deadline_list_id = data.pop("deadline_list_id", None)
    assigned_to_id = data.pop("assigned_to_id", None)

    for attr, value in data.items():
        setattr(deadline, attr, value)

    if deadline_list_id:
        deadline_list = get_object_or_404(DeadlineList, id=deadline_list_id, is_deleted=False)
        deadline.deadline_list = deadline_list

    if assigned_to_id:
        assigned_to = get_object_or_404(User, id=assigned_to_id)
        deadline.assigned_to = assigned_to

    if request.user.is_authenticated:
        deadline.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            deadline.updated_by = admin_user

    deadline.save()

    return {
        "id": deadline.id,
        "name": deadline.name,
        "slug": deadline.slug,
        "description": deadline.description,
        "deadline_list_id": deadline.deadline_list.id if deadline.deadline_list else None,
        "deadline_list_name": deadline.deadline_list.name if deadline.deadline_list else None,
        "due_date": deadline.due_date,
        "assigned_to_id": deadline.assigned_to.id if deadline.assigned_to else None,
        "assigned_to_name": deadline.assigned_to.get_full_name() if deadline.assigned_to else None,
        "completed": deadline.completed,
        "completed_at": deadline.completed_at,
        "completed_note": deadline.completed_note,
        "overdue": deadline.overdue_status(),
        "created_by_id": deadline.created_by.id if deadline.created_by else None,
        "created_by_name": deadline.created_by.get_full_name() if deadline.created_by else None,
        "updated_by_id": deadline.updated_by.id if deadline.updated_by else None,
        "updated_by_name": deadline.updated_by.get_full_name() if deadline.updated_by else None,
        "created_at": deadline.created_at,
        "updated_at": deadline.updated_at,
    }


@router.delete("/deadlines/{deadline_id}")
def delete_deadline(request, deadline_id: UUID):
    """Soft delete a deadline"""
    deadline = get_object_or_404(Deadline, id=deadline_id, is_deleted=False)
    deadline.is_deleted = True
    if request.user.is_authenticated:
        deadline.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            deadline.updated_by = admin_user
    deadline.save()
    return {"success": True, "message": "Deadline deleted successfully"}
