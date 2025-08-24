import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from users.models import User


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True, help_text="Contact's website URL")
    category = models.CharField(
        max_length=100, blank=True, null=True, help_text="Contact category (e.g., Vendor, Guest, Venue)"
    )
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_contact", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_contact", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        if self.company:
            if self.name:
                return f"{self.name} ({self.company})"
            else:
                return self.company
        return self.name

    def clean(self):
        super().clean()
        if not self.name and not self.company:
            raise ValidationError("Either name or company must be provided.")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Contacts"
        constraints = [models.UniqueConstraint(fields=["name", "company"], name="unique_contact")]

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            slug_base = self.name or self.company
            self.slug = slugify(slug_base)
        super().save(*args, **kwargs)


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    contact = models.ForeignKey(Contact, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to="contact_files/")
    uploaded_by = models.ForeignKey(User, related_name="files_uploaded_by", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_file", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name or self.file.name

    class Meta:
        verbose_name_plural = "Contact Files"
        ordering = ["-uploaded_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while File.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
