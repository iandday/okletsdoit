import uuid

from django.db import models
from simple_history.models import HistoricalRecords


class UploadedPhoto(models.Model):
    """A photo that has been uploaded by a user"""

    class STATUS_CHOICES(models.TextChoices):
        PENDING = "Pending", "Pending"
        PROCESSING = "Processing", "Processing"
        READY = "Ready", "Ready"
        FAILED = "Failed", "Failed"
        REJECTED = "Rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo_file = models.ImageField(upload_to="photos/")
    thumbnail_file = models.ImageField(upload_to="photos/thumbnails/", null=True, blank=True)
    content_type = models.CharField(max_length=255, null=True, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    camera = models.CharField(max_length=255, null=True, blank=True)
    checksum = models.CharField(max_length=64, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    favorite_count = models.PositiveIntegerField(default=0)
    flagged = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES.choices,
        default=STATUS_CHOICES.PENDING,
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ["uploaded_at"]
        verbose_name_plural = "Uploaded Photos"

    def get_storage_object_key(self) -> str:
        return f"media/photos/{self.id}.jpg"

    def get_photo_storage_path(self) -> str:
        return f"photos/{self.id}.jpg"

    def __str__(self):
        return self.photo_file.name or f"UploadedPhoto {self.id}"
