import datetime
import uuid

from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from users.models import User




class Idea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_idea", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_idea", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Ideas"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_idea")]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
