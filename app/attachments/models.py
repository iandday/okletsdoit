import uuid
from pathlib import Path

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords
from users.models import User


def attachment_upload_path(instance, filename: str) -> str:
    """
    Generates a file upload path for an attachment based on the related object's app label, model name, and primary key.
    Args:
        instance: The attachment instance, expected to have a 'content_object' attribute referencing the related model.
        filename (str): The name of the file being uploaded.
    Returns:
        str: A formatted string representing the upload path, in the form 'attachments/{app}_{model}/{pk}/{filename}'.
    """

    return "attachments/{app}_{model}/{pk}/{filename}".format(
        app=instance.content_object._meta.app_label,
        model=instance.content_object._meta.object_name.lower(),
        pk=instance.content_object.pk,
        filename=filename,
    )


class AttachmentManager(models.Manager):
    def attachments_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id, object_id=obj.pk)


class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    attachment_file = models.FileField(upload_to=attachment_upload_path)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")
    object_id = models.UUIDField(db_index=True)
    uploaded_by = models.ForeignKey(User, related_name="attachment_uploaded_by", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="attachment_updated_by", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = AttachmentManager()
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name or self.attachment_file.name

    class Meta:
        verbose_name_plural = "Attachments"
        verbose_name = "Attachment"
        ordering = ["-uploaded_at"]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Attachment.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        if self.content_object:
            self.content_type = ContentType.objects.get_for_model(self.content_object)

        super().save(*args, **kwargs)

    @property
    def filename(self) -> str:
        return Path(self.attachment_file.name).name

    def attach_to(self, new_object: models.Model) -> None:
        self.object_id = new_object.pk

        self.save()

        old_path = self.attachment_file.path
        self.attachment_file.name = attachment_upload_path(self, self.filename)
        self.attachment_file.save()

        old_path = Path(old_path)
        new_path = Path(self.attachment_file.path)

        if old_path != new_path:
            new_path.parent.mkdir(parents=True, exist_ok=True)
            old_path.rename(new_path)
