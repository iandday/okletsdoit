from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import FilterSchema
from ninja import Query
from ninja import Router
from ninja import Schema
from ninja.files import UploadedFile
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate

from core.auth import multi_auth

from .models import Attachment

User = get_user_model()

router = Router(tags=["Attachments"], auth=multi_auth)


# Schemas
class AttachmentSchema(Schema):
    id: UUID
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    filename: str
    file_url: str
    content_type_id: int
    content_type_app_label: str
    content_type_model: str
    object_id: UUID
    uploaded_by_id: Optional[UUID] = None
    uploaded_by_name: Optional[str] = None
    updated_by_id: Optional[UUID] = None
    updated_by_name: Optional[str] = None
    uploaded_at: datetime
    updated_at: datetime


class AttachmentFilterSchema(FilterSchema):
    content_type_id: Optional[int] = None
    object_id: Optional[UUID] = None
    search: Optional[str] = None


class AttachmentCreateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    content_type_id: int
    object_id: UUID


class AttachmentUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None


class ContentTypeSchema(Schema):
    id: int
    app_label: str
    model: str


# Helper endpoint to get content type ID
@router.get("/content-types/{app_label}/{model}", response=ContentTypeSchema)
def get_content_type(request, app_label: str, model: str):
    """Get content type ID for a given app and model"""
    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model.lower())
        return {
            "id": content_type.id,
            "app_label": content_type.app_label,
            "model": content_type.model,
        }
    except ContentType.DoesNotExist:
        from django.http import Http404

        raise Http404(f"Content type not found for {app_label}.{model}")


# Attachment CRUD Endpoints
@router.get("/attachments", response=List[AttachmentSchema])
@paginate(PageNumberPagination, page_size=50)
def list_attachments(request, filters: AttachmentFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all attachments (non-deleted) with filtering"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()

    # Add search functionality for name and description
    if filters.search:
        q &= Q(name__icontains=filters.search) | Q(description__icontains=filters.search)

    attachments = (
        Attachment.objects.filter(q)
        .select_related("content_type", "uploaded_by", "updated_by")
        .order_by("-uploaded_at")
    )

    return [
        {
            "id": attachment.id,
            "name": attachment.name,
            "slug": attachment.slug,
            "description": attachment.description,
            "filename": attachment.filename,
            "file_url": attachment.attachment_file.url if attachment.attachment_file else "",
            "content_type_id": attachment.content_type.id,
            "content_type_app_label": attachment.content_type.app_label,
            "content_type_model": attachment.content_type.model,
            "object_id": attachment.object_id,
            "uploaded_by_id": attachment.uploaded_by.id if attachment.uploaded_by else None,
            "uploaded_by_name": attachment.uploaded_by.get_full_name() if attachment.uploaded_by else None,
            "updated_by_id": attachment.updated_by.id if attachment.updated_by else None,
            "updated_by_name": attachment.updated_by.get_full_name() if attachment.updated_by else None,
            "uploaded_at": attachment.uploaded_at,
            "updated_at": attachment.updated_at,
        }
        for attachment in attachments
    ]


@router.get("/attachments/{attachment_id}", response=AttachmentSchema)
def get_attachment(request, attachment_id: UUID):
    """Get a specific attachment by ID"""
    attachment = get_object_or_404(Attachment, id=attachment_id, is_deleted=False)
    return {
        "id": attachment.id,
        "name": attachment.name,
        "slug": attachment.slug,
        "description": attachment.description,
        "filename": attachment.filename,
        "file_url": attachment.attachment_file.url if attachment.attachment_file else "",
        "content_type_id": attachment.content_type.id,
        "content_type_app_label": attachment.content_type.app_label,
        "content_type_model": attachment.content_type.model,
        "object_id": attachment.object_id,
        "uploaded_by_id": attachment.uploaded_by.id if attachment.uploaded_by else None,
        "uploaded_by_name": attachment.uploaded_by.get_full_name() if attachment.uploaded_by else None,
        "updated_by_id": attachment.updated_by.id if attachment.updated_by else None,
        "updated_by_name": attachment.updated_by.get_full_name() if attachment.updated_by else None,
        "uploaded_at": attachment.uploaded_at,
        "updated_at": attachment.updated_at,
    }


@router.post("/attachments", response=AttachmentSchema)
def create_attachment(
    request,
    file: UploadedFile,
    content_type_id: int,
    object_id: UUID,
    name: Optional[str] = None,
    description: Optional[str] = None,
):
    """Create a new attachment with file upload"""
    content_type = get_object_or_404(ContentType, id=content_type_id)

    data = {
        "name": name or file.name,
        "description": description,
        "attachment_file": file,
        "content_type": content_type,
        "object_id": object_id,
    }

    if request.user.is_authenticated:
        data["uploaded_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["uploaded_by"] = admin_user

    attachment = Attachment.objects.create(**data)

    return {
        "id": attachment.id,
        "name": attachment.name,
        "slug": attachment.slug,
        "description": attachment.description,
        "filename": attachment.filename,
        "file_url": attachment.attachment_file.url if attachment.attachment_file else "",
        "content_type_id": attachment.content_type.id,
        "content_type_app_label": attachment.content_type.app_label,
        "content_type_model": attachment.content_type.model,
        "object_id": attachment.object_id,
        "uploaded_by_id": attachment.uploaded_by.id if attachment.uploaded_by else None,
        "uploaded_by_name": attachment.uploaded_by.get_full_name() if attachment.uploaded_by else None,
        "updated_by_id": attachment.updated_by.id if attachment.updated_by else None,
        "updated_by_name": attachment.updated_by.get_full_name() if attachment.updated_by else None,
        "uploaded_at": attachment.uploaded_at,
        "updated_at": attachment.updated_at,
    }


@router.put("/attachments/{attachment_id}", response=AttachmentSchema)
def update_attachment(request, attachment_id: UUID, payload: AttachmentUpdateSchema):
    """Update an attachment"""
    attachment = get_object_or_404(Attachment, id=attachment_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)

    for attr, value in data.items():
        setattr(attachment, attr, value)

    if request.user.is_authenticated:
        attachment.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            attachment.updated_by = admin_user

    attachment.save()

    return {
        "id": attachment.id,
        "name": attachment.name,
        "slug": attachment.slug,
        "description": attachment.description,
        "filename": attachment.filename,
        "file_url": attachment.attachment_file.url if attachment.attachment_file else "",
        "content_type_id": attachment.content_type.id,
        "content_type_app_label": attachment.content_type.app_label,
        "content_type_model": attachment.content_type.model,
        "object_id": attachment.object_id,
        "uploaded_by_id": attachment.uploaded_by.id if attachment.uploaded_by else None,
        "uploaded_by_name": attachment.uploaded_by.get_full_name() if attachment.uploaded_by else None,
        "updated_by_id": attachment.updated_by.id if attachment.updated_by else None,
        "updated_by_name": attachment.updated_by.get_full_name() if attachment.updated_by else None,
        "uploaded_at": attachment.uploaded_at,
        "updated_at": attachment.updated_at,
    }


@router.delete("/attachments/{attachment_id}")
def delete_attachment(request, attachment_id: UUID):
    """Soft delete an attachment"""
    attachment = get_object_or_404(Attachment, id=attachment_id, is_deleted=False)
    attachment.is_deleted = True
    if request.user.is_authenticated:
        attachment.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            attachment.updated_by = admin_user
    attachment.save()
    return {"success": True, "message": "Attachment deleted successfully"}
