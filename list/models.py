import uuid

from django.db import models
from django.utils.text import slugify

from users.models import User


class List(models.Model):
    """A list that contains multiple list entries"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_list", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_list", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Lists"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_list")]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while List.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def total_entries(self):
        """Return total number of entries in this list"""
        return self.entries.filter(is_deleted=False).count()

    @property
    def completed_entries(self):
        """Return number of completed entries in this list"""
        return self.entries.filter(is_completed=True, is_deleted=False).count()

    @property
    def pending_entries(self):
        """Return number of pending entries in this list"""
        return self.entries.filter(is_completed=False, is_deleted=False).count()

    @property
    def completion_percentage(self):
        """Return completion percentage of this list"""
        if self.total_entries == 0:
            return 0
        return round((self.completed_entries / self.total_entries) * 100, 1)


class ListEntry(models.Model):
    """An individual entry within a list"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="entries")
    order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_list_entry", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_list_entry", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["order", "item"]
        verbose_name_plural = "List Entries"
        constraints = [models.UniqueConstraint(fields=["item", "list"], name="unique_list_entry_item_list")]

    def __str__(self):
        return self.item

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.item)
            slug = base_slug
            counter = 1

            while ListEntry.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # update completed_at if is_completed is True
        if self.is_completed and not self.completed_at:
            self.completed_at = self.updated_at.date()
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)
