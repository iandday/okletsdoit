import datetime
import uuid
from django.db import models

from users.models import User


class TaskList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    created_by = models.ForeignKey(User, related_name="created_by_task_list", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_task_list", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Task Lists"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_task_list")]


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_task", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_task", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        User, related_name="assigned_to_task", on_delete=models.CASCADE, blank=True, null=True
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    completed_note = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        return True if self.due_date and datetime.date.today() > self.due_date else False

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        # If Task is being marked complete, set the completed_date
        if self.completed:
            self.completed_at = datetime.datetime.now()
        super(Task, self).save()

    class Meta:
        ordering = ["priority", "created_at"]
