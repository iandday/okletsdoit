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

from .models import Contact

User = get_user_model()

router = Router(tags=["Contacts"], auth=multi_auth)


# Schemas
class ContactSchema(Schema):
    id: UUID
    name: Optional[str] = None
    slug: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    created_by_id: Optional[UUID] = None
    created_by_name: Optional[str] = None
    updated_by_id: Optional[UUID] = None
    updated_by_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ContactFilterSchema(FilterSchema):
    category: Optional[str] = None
    search: Optional[str] = None


class ContactCreateSchema(Schema):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None


class ContactUpdateSchema(Schema):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None


# Contact CRUD Endpoints
@router.get("/contacts", response=List[ContactSchema])
@paginate(PageNumberPagination, page_size=50)
def list_contacts(request, filters: ContactFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all contacts (non-deleted) with filtering"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()

    # Add search functionality for name, company, and email
    if filters.search:
        q &= (
            Q(name__icontains=filters.search)
            | Q(company__icontains=filters.search)
            | Q(email__icontains=filters.search)
        )

    contacts = Contact.objects.filter(q).select_related("created_by", "updated_by").order_by("name")

    return [
        {
            "id": contact.id,
            "name": contact.name,
            "slug": contact.slug,
            "company": contact.company,
            "email": contact.email,
            "phone": contact.phone,
            "website": contact.website,
            "category": contact.category,
            "notes": contact.notes,
            "created_by_id": contact.created_by.id if contact.created_by else None,
            "created_by_name": contact.created_by.get_full_name() if contact.created_by else None,
            "updated_by_id": contact.updated_by.id if contact.updated_by else None,
            "updated_by_name": contact.updated_by.get_full_name() if contact.updated_by else None,
            "created_at": contact.created_at,
            "updated_at": contact.updated_at,
        }
        for contact in contacts
    ]


@router.get("/contacts/{contact_id}", response=ContactSchema)
def get_contact(request, contact_id: UUID):
    """Get a specific contact by ID"""
    contact = get_object_or_404(Contact, id=contact_id, is_deleted=False)
    return {
        "id": contact.id,
        "name": contact.name,
        "slug": contact.slug,
        "company": contact.company,
        "email": contact.email,
        "phone": contact.phone,
        "website": contact.website,
        "category": contact.category,
        "notes": contact.notes,
        "created_by_id": contact.created_by.id if contact.created_by else None,
        "created_by_name": contact.created_by.get_full_name() if contact.created_by else None,
        "updated_by_id": contact.updated_by.id if contact.updated_by else None,
        "updated_by_name": contact.updated_by.get_full_name() if contact.updated_by else None,
        "created_at": contact.created_at,
        "updated_at": contact.updated_at,
    }


@router.post("/contacts", response=ContactSchema)
def create_contact(request, payload: ContactCreateSchema):
    """Create a new contact"""
    data = payload.dict()

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    contact = Contact.objects.create(**data)

    return {
        "id": contact.id,
        "name": contact.name,
        "slug": contact.slug,
        "company": contact.company,
        "email": contact.email,
        "phone": contact.phone,
        "website": contact.website,
        "category": contact.category,
        "notes": contact.notes,
        "created_by_id": contact.created_by.id if contact.created_by else None,
        "created_by_name": contact.created_by.get_full_name() if contact.created_by else None,
        "updated_by_id": contact.updated_by.id if contact.updated_by else None,
        "updated_by_name": contact.updated_by.get_full_name() if contact.updated_by else None,
        "created_at": contact.created_at,
        "updated_at": contact.updated_at,
    }


@router.put("/contacts/{contact_id}", response=ContactSchema)
def update_contact(request, contact_id: UUID, payload: ContactUpdateSchema):
    """Update a contact"""
    contact = get_object_or_404(Contact, id=contact_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)

    for attr, value in data.items():
        setattr(contact, attr, value)

    if request.user.is_authenticated:
        contact.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            contact.updated_by = admin_user

    contact.save()

    return {
        "id": contact.id,
        "name": contact.name,
        "slug": contact.slug,
        "company": contact.company,
        "email": contact.email,
        "phone": contact.phone,
        "website": contact.website,
        "category": contact.category,
        "notes": contact.notes,
        "created_by_id": contact.created_by.id if contact.created_by else None,
        "created_by_name": contact.created_by.get_full_name() if contact.created_by else None,
        "updated_by_id": contact.updated_by.id if contact.updated_by else None,
        "updated_by_name": contact.updated_by.get_full_name() if contact.updated_by else None,
        "created_at": contact.created_at,
        "updated_at": contact.updated_at,
    }


@router.delete("/contacts/{contact_id}")
def delete_contact(request, contact_id: UUID):
    """Soft delete a contact"""
    contact = get_object_or_404(Contact, id=contact_id, is_deleted=False)
    contact.is_deleted = True
    if request.user.is_authenticated:
        contact.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            contact.updated_by = admin_user
    contact.save()
    return {"success": True, "message": "Contact deleted successfully"}
