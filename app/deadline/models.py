import datetime
import uuid

from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from users.models import User


class DeadlineList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    created_by = models.ForeignKey(User, related_name="created_by_deadline_list", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_deadline_list", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    @property
    def completed_count(self):
        return self.deadline_set.filter(completed=True, is_deleted=False).count()

    @property
    def pending_count(self):
        return self.deadline_set.filter(completed=False, is_deleted=False).count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Task Lists"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_deadline_list")]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while DeadlineList.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Deadline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    deadline_list = models.ForeignKey(DeadlineList, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_deadline", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_deadline", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        User, related_name="assigned_to_deadline", on_delete=models.CASCADE, blank=True, null=True
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    completed_note = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        return True if self.due_date and datetime.date.today() > self.due_date else False

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # If Deadline is being marked complete, set the completed_date
        if self.completed and not self.completed_at:
            self.completed_at = datetime.datetime.now()

        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while DeadlineList.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["due_date", "created_at"]
