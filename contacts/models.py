import uuid
from django.db import models
from django.utils.text import slugify
from users.models import User


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Contacts"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_contact")]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_display_name(self):
        """Return name with company if available"""
        if self.company:
            return f"{self.name} ({self.company})"
        return self.name
