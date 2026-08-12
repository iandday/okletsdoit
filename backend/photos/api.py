import hashlib
import io
import zipfile
from datetime import datetime
from typing import List as TypeList
from typing import Optional
from uuid import UUID

import boto3
from botocore.exceptions import ClientError
from core.auth import multi_auth
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja import Schema
from ninja.errors import HttpError
from PIL import Image
from PIL import ImageOps
from PIL import UnidentifiedImageError

from .models import UploadedPhoto
from .realtime import publish_photo_update

router = Router(tags=["Uploaded Photos"])

THUMBNAIL_MAX_DIMENSION = 256

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
    HEIF_ENABLED = True
except Exception:
    HEIF_ENABLED = False


class UploadedPhotoSchema(Schema):
    id: UUID
    photo_file: str
    thumbnail_file: Optional[str]
    content_type: Optional[str]
    file_size: Optional[int]
    width: Optional[int]
    height: Optional[int]
    camera: Optional[str]
    checksum: Optional[str]
    uploaded_at: datetime
    is_approved: bool
    is_deleted: bool
    favorite_count: int
    flagged: bool
    status: str


class CreateUploadedPhotoResponseSchema(Schema):
    id: UUID
    upload_url: str


class CompleteUploadedPhotoResponseSchema(Schema):
    id: UUID
    status: str


@router.get("/uploaded/{photo_id}/download")
def download_uploaded_photo(request, photo_id: UUID):
    """Return a short-lived attachment URL for downloading a photo file."""
    photo = get_object_or_404(UploadedPhoto, id=photo_id, is_deleted=False, status=UploadedPhoto.STATUS_CHOICES.READY)

    bucket_name = settings.STORAGES["default"]["OPTIONS"]["bucket_name"]
    object_key = photo.get_storage_object_key()
    file_name = f"photo-{photo.id}.jpg"

    s3_client = boto3.client(
        "s3",
        region_name=settings.STORAGES["default"]["OPTIONS"].get("region_name"),
        aws_access_key_id=settings.STORAGES["default"]["OPTIONS"].get("access_key"),
        aws_secret_access_key=settings.STORAGES["default"]["OPTIONS"].get("secret_key"),
        endpoint_url=settings.STORAGES["default"]["OPTIONS"].get("endpoint_url"),
    )

    download_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_key,
            "ResponseContentDisposition": f'attachment; filename="{file_name}"',
        },
        ExpiresIn=3600,
    )

    return HttpResponseRedirect(download_url)


@router.post("/create", response=CreateUploadedPhotoResponseSchema)
def create_uploaded_photo(request):
    """
    Create a pending uploaded-photo record and return a presigned upload URL.
    """
    photo = UploadedPhoto.objects.create(
        photo_file="photos/original",
        status=UploadedPhoto.STATUS_CHOICES.PENDING,
    )

    bucket_name = settings.STORAGES["default"]["OPTIONS"]["bucket_name"]
    object_key = photo.get_storage_object_key()

    photo.photo_file.name = photo.get_photo_storage_path()
    photo.save(update_fields=["photo_file"])

    s3_client = boto3.client(
        "s3",
        region_name=settings.STORAGES["default"]["OPTIONS"].get("region_name"),
        aws_access_key_id=settings.STORAGES["default"]["OPTIONS"].get("access_key"),
        aws_secret_access_key=settings.STORAGES["default"]["OPTIONS"].get("secret_key"),
        endpoint_url=settings.STORAGES["default"]["OPTIONS"].get("endpoint_url"),
    )

    params = {
        "Bucket": bucket_name,
        "Key": object_key,
    }

    upload_url = s3_client.generate_presigned_url(
        "put_object",
        Params=params,
        ExpiresIn=3600,
    )

    return {
        "id": photo.id,
        "upload_url": upload_url,
    }


@router.post("/uploaded/{photo_id}/complete", response=CompleteUploadedPhotoResponseSchema)
def complete_uploaded_photo(request, photo_id: UUID):
    """
    Process the uploaded photo
    """
    photo = get_object_or_404(UploadedPhoto, id=photo_id, is_deleted=False)
    photo.status = UploadedPhoto.STATUS_CHOICES.PROCESSING
    photo.save(update_fields=["status"])

    bucket_name = settings.STORAGES["default"]["OPTIONS"]["bucket_name"]
    object_key = photo.get_storage_object_key()
    s3_client = boto3.client(
        "s3",
        region_name=settings.STORAGES["default"]["OPTIONS"].get("region_name"),
        aws_access_key_id=settings.STORAGES["default"]["OPTIONS"].get("access_key"),
        aws_secret_access_key=settings.STORAGES["default"]["OPTIONS"].get("secret_key"),
        endpoint_url=settings.STORAGES["default"]["OPTIONS"].get("endpoint_url"),
    )

    raw_bytes = b""
    try:
        mem_buffer = io.BytesIO()
        s3_client.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=mem_buffer)
        raw_bytes = mem_buffer.getvalue()
        checksum = hashlib.sha256(raw_bytes).hexdigest()

        with Image.open(io.BytesIO(raw_bytes)) as img:
            exif = img.getexif() or {}
            make = (exif.get(271) or "").strip()
            model = (exif.get(272) or "").strip()
            camera = " ".join(part for part in [make, model] if part) or None

            img = ImageOps.exif_transpose(img)
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            elif img.mode == "L":
                img = img.convert("RGB")

            processed = img.copy()
            processed.thumbnail((2048, 2048), Image.Resampling.LANCZOS)

            processed_buffer = io.BytesIO()
            processed.save(processed_buffer, format="JPEG", quality=90, optimize=True)
            processed_bytes = processed_buffer.getvalue()

            thumb = processed.copy()
            thumb.thumbnail((THUMBNAIL_MAX_DIMENSION, THUMBNAIL_MAX_DIMENSION), Image.Resampling.LANCZOS)
            thumb_buffer = io.BytesIO()
            thumb.save(thumb_buffer, format="JPEG", quality=85, optimize=True)
            thumb_bytes = thumb_buffer.getvalue()

            width, height = processed.size

        photo.photo_file.save(photo.get_photo_storage_path(), ContentFile(processed_bytes), save=False)
        thumbnail_name = f"photos/thumbnails/{photo.id}.jpg"
        photo.thumbnail_file.save(thumbnail_name, ContentFile(thumb_bytes), save=False)

        photo.content_type = "image/jpeg"
        photo.file_size = len(processed_bytes)
        photo.width = width
        photo.height = height
        photo.camera = camera
        photo.checksum = checksum
        photo.status = UploadedPhoto.STATUS_CHOICES.READY
        photo.save(
            update_fields=[
                "photo_file",
                "thumbnail_file",
                "content_type",
                "file_size",
                "width",
                "height",
                "camera",
                "checksum",
                "status",
            ]
        )

        publish_photo_update(
            event="photo.ready",
            photo_id=str(photo.id),
            status=photo.status,
            uploaded_at=photo.uploaded_at.isoformat() if photo.uploaded_at else None,
        )

        return {
            "id": photo.id,
            "status": photo.status,
        }
    except (ClientError, UnidentifiedImageError, OSError) as exc:
        photo.status = UploadedPhoto.STATUS_CHOICES.FAILED
        photo.save(update_fields=["status"])
        publish_photo_update(event="photo.failed", photo_id=str(photo.id), status=photo.status)
        looks_like_heif = False
        if len(raw_bytes) >= 12:
            # HEIF/HEIC uses ISO BMFF brand in the ftyp box (bytes 8-12).
            major_brand = raw_bytes[8:12]
            looks_like_heif = major_brand in {b"heic", b"heix", b"hevc", b"hevx", b"mif1", b"msf1"}

        if isinstance(exc, UnidentifiedImageError) and looks_like_heif and not HEIF_ENABLED:
            raise HttpError(400, "HEIC/HEIF image support is not available on the server.")
        raise HttpError(400, f"Unable to process uploaded photo: {exc}")
    except Exception as exc:
        photo.status = UploadedPhoto.STATUS_CHOICES.FAILED
        photo.save(update_fields=["status"])
        publish_photo_update(event="photo.failed", photo_id=str(photo.id), status=photo.status)
        raise HttpError(500, f"Unexpected error while processing uploaded photo: {exc}")


@router.get("/list", response=TypeList[UploadedPhotoSchema])
def list_uploaded_photos(request):
    """
    List all uploaded photos.
    """
    photos = UploadedPhoto.objects.filter(
        is_deleted=False, is_approved=True, status=UploadedPhoto.STATUS_CHOICES.READY
    ).order_by("-uploaded_at")
    return photos


@router.get("/all", response=TypeList[UploadedPhotoSchema], auth=multi_auth)
def list_all_uploaded_photos(request):
    """
    List all uploaded photos for admin review, including soft-deleted records.
    """
    photos = UploadedPhoto.objects.filter(status=UploadedPhoto.STATUS_CHOICES.READY).order_by("-uploaded_at")
    return photos


@router.post("/uploaded/{photo_id}/update", response=UploadedPhotoSchema, auth=multi_auth)
def update_uploaded_photo(request, photo_id: UUID, data: UploadedPhotoSchema):
    """
    Update an uploaded photo's metadata.
    """
    photo = get_object_or_404(UploadedPhoto, id=photo_id)
    for field in ["is_approved", "flagged", "is_deleted", "favorite_count"]:
        if hasattr(data, field):
            setattr(photo, field, getattr(data, field))
    photo.save(update_fields=["is_approved", "flagged", "is_deleted", "favorite_count"])
    publish_photo_update(
        event="photo.updated",
        photo_id=str(photo.id),
        status=photo.status,
        uploaded_at=photo.uploaded_at.isoformat() if photo.uploaded_at else None,
    )
    return photo


# endpoint to download all uploaded photos as a zip file
@router.get(
    "/export_all",
    auth=multi_auth,
    response=None,
    openapi_extra={
        "responses": {
            200: {
                "description": "Zip file containing all uploaded photos",
                "content": {
                    "application/zip": {"schema": {"type": "string", "format": "binary"}},
                },
            }
        }
    },
)
def export_all_uploaded_photos(request):
    """
    Export all uploaded photos as a zip file.
    """

    photos = UploadedPhoto.objects.filter(
        is_deleted=False, is_approved=True, status=UploadedPhoto.STATUS_CHOICES.READY
    ).order_by("-uploaded_at")

    bucket_name = settings.STORAGES["default"]["OPTIONS"]["bucket_name"]
    s3_client = boto3.client(
        "s3",
        region_name=settings.STORAGES["default"]["OPTIONS"].get("region_name"),
        aws_access_key_id=settings.STORAGES["default"]["OPTIONS"].get("access_key"),
        aws_secret_access_key=settings.STORAGES["default"]["OPTIONS"].get("secret_key"),
        endpoint_url=settings.STORAGES["default"]["OPTIONS"].get("endpoint_url"),
    )

    with io.BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for photo in photos:
                object_key = photo.get_storage_object_key()
                mem_buffer = io.BytesIO()
                s3_client.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=mem_buffer)
                mem_buffer.seek(0)
                zip_file.writestr(f"{photo.id}.jpg", mem_buffer.read())
        zip_bytes = zip_buffer.getvalue()

    async def stream_zip():
        chunk_size = 64 * 1024
        for index in range(0, len(zip_bytes), chunk_size):
            yield zip_bytes[index : index + chunk_size]

    response = StreamingHttpResponse(stream_zip(), content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="uploaded_photos.zip"'
    return response
