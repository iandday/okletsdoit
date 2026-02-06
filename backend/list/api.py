import logging
from datetime import datetime, date
from typing import List as TypeList
from typing import Optional
from uuid import UUID
from decimal import Decimal

from core.auth import multi_auth
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import FilterSchema
from ninja import Query
from ninja import Router
from ninja import Schema
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate

from .models import List, ListEntry

router = Router(tags=["List"], auth=multi_auth)

logger = logging.getLogger(__name__)

User = get_user_model()


# List Schemas
class ListSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    total_entries: int
    completed_entries: int
    pending_entries: int
    completion_percentage: float

    @staticmethod
    def resolve_total_entries(obj):
        return obj.total_entries

    @staticmethod
    def resolve_completed_entries(obj):
        return obj.completed_entries

    @staticmethod
    def resolve_pending_entries(obj):
        return obj.pending_entries

    @staticmethod
    def resolve_completion_percentage(obj):
        return obj.completion_percentage


class ListFilterSchema(FilterSchema):
    name: Optional[str] = None


class ListCreateSchema(Schema):
    name: str
    description: Optional[str] = ""


class ListUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None


# ListEntry Schemas
class ListEntrySchema(Schema):
    id: UUID
    item: str
    slug: str
    description: Optional[str] = None
    list_id: UUID
    order: int
    is_completed: bool
    completed_at: Optional[date] = None
    purchased: bool
    vendor_id: Optional[UUID] = None
    associated_expense_id: Optional[UUID] = None
    quantity: int
    unit_price: Decimal
    additional_price: Decimal
    total_price: Decimal
    url: Optional[str] = None
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ListEntryFilterSchema(FilterSchema):
    item: Optional[str] = None
    list_id: Optional[UUID] = None
    is_completed: Optional[bool] = None
    purchased: Optional[bool] = None
    vendor_id: Optional[UUID] = None
    associated_expense_id: Optional[UUID] = None


class ListEntryCreateSchema(Schema):
    item: str
    description: Optional[str] = ""
    list_id: UUID
    order: Optional[int] = 0
    is_completed: Optional[bool] = False
    purchased: Optional[bool] = False
    vendor_id: Optional[UUID] = None
    associated_expense_id: Optional[UUID] = None
    quantity: Optional[int] = 1
    unit_price: Optional[Decimal] = Decimal("0.00")
    additional_price: Optional[Decimal] = Decimal("0.00")
    url: Optional[str] = None


class ListEntryUpdateSchema(Schema):
    item: Optional[str] = None
    description: Optional[str] = None
    list_id: Optional[UUID] = None
    order: Optional[int] = None
    is_completed: Optional[bool] = None
    purchased: Optional[bool] = None
    vendor_id: Optional[UUID] = None
    associated_expense_id: Optional[UUID] = None
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    additional_price: Optional[Decimal] = None
    url: Optional[str] = None


# List CRUD Endpoints
@router.get("/lists", response=TypeList[ListSchema])
@paginate(PageNumberPagination, page_size=50)
def list_lists(request, filters: ListFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all lists (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    return List.objects.filter(q).order_by("-created_at")


@router.get("/lists/{list_id}", response=ListSchema)
def get_list(request, list_id: UUID):
    """Get a specific list by ID"""
    return get_object_or_404(List, id=list_id, is_deleted=False)


@router.post("/lists", response=ListSchema)
def create_list(request, payload: ListCreateSchema):
    """Create a new list"""
    data = payload.dict()
    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user
    list_obj = List.objects.create(**data)
    return list_obj


@router.put("/lists/{list_id}", response=ListSchema)
def update_list(request, list_id: UUID, payload: ListUpdateSchema):
    """Update a list"""
    list_obj = get_object_or_404(List, id=list_id, is_deleted=False)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(list_obj, attr, value)

    if request.user.is_authenticated:
        list_obj.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            list_obj.updated_by = admin_user
    list_obj.save()
    return list_obj


@router.delete("/lists/{list_id}")
def delete_list(request, list_id: UUID):
    """Soft delete a list"""
    list_obj = get_object_or_404(List, id=list_id, is_deleted=False)
    list_obj.is_deleted = True
    if request.user.is_authenticated:
        list_obj.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            list_obj.updated_by = admin_user
    list_obj.save()
    return {"success": True, "message": "List deleted successfully"}


# ListEntry CRUD Endpoints
@router.get("/list-entries", response=TypeList[ListEntrySchema])
@paginate(PageNumberPagination, page_size=50)
def list_list_entries(request, filters: ListEntryFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all list entries (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    return ListEntry.objects.filter(q).order_by("order", "item")


@router.get("/list-entries/{entry_id}", response=ListEntrySchema)
def get_list_entry(request, entry_id: UUID):
    """Get a specific list entry by ID"""
    return get_object_or_404(ListEntry, id=entry_id, is_deleted=False)


@router.post("/list-entries", response=ListEntrySchema)
def create_list_entry(request, payload: ListEntryCreateSchema):
    """Create a new list entry"""
    data = payload.dict()
    list_id = data.pop("list_id")

    # Validate list_id
    get_object_or_404(List, id=list_id, is_deleted=False)

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    entry = ListEntry.objects.create(
        **data,
        list_id=list_id,
    )
    return entry


@router.put("/list-entries/{entry_id}", response=ListEntrySchema)
def update_list_entry(request, entry_id: UUID, payload: ListEntryUpdateSchema):
    """Update a list entry"""
    entry = get_object_or_404(ListEntry, id=entry_id, is_deleted=False)

    data = payload.dict(exclude_unset=True)
    # Validate list_id if it's being changed
    if "list_id" in data:
        get_object_or_404(List, id=data["list_id"], is_deleted=False)

    for attr, value in data.items():
        setattr(entry, attr, value)

    if request.user.is_authenticated:
        entry.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            entry.updated_by = admin_user
    entry.save()
    return entry


@router.delete("/list-entries/{entry_id}")
def delete_list_entry(request, entry_id: UUID):
    """Soft delete a list entry"""
    entry = get_object_or_404(ListEntry, id=entry_id, is_deleted=False)
    entry.is_deleted = True
    if request.user.is_authenticated:
        entry.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            entry.updated_by = admin_user
    entry.save()
    return {"success": True, "message": "List entry deleted successfully"}


@router.post("/list-entries/{entry_id}/toggle-completed", response=ListEntrySchema)
def toggle_completed(request, entry_id: UUID):
    """Toggle the completed status of a list entry"""
    entry = get_object_or_404(ListEntry, id=entry_id, is_deleted=False)
    entry.is_completed = not entry.is_completed
    if request.user.is_authenticated:
        entry.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            entry.updated_by = admin_user
    entry.save()
    return entry


@router.post("/list-entries/{entry_id}/toggle-purchased", response=ListEntrySchema)
def toggle_purchased(request, entry_id: UUID):
    """Toggle the purchased status of a list entry"""
    entry = get_object_or_404(ListEntry, id=entry_id, is_deleted=False)
    entry.purchased = not entry.purchased
    if request.user.is_authenticated:
        entry.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            entry.updated_by = admin_user
    entry.save()
    return entry
