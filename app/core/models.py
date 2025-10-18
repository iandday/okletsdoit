import datetime
import uuid

from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords
from typing import Any
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
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Idea.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Timeline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100)
    start = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False, help_text="Indicates if the event is published to the venue page")
    confirmed = models.BooleanField(default=False, help_text="Indicates if the event is confirmed")
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_timeline_event", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_timeline_event", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["start"]
        verbose_name_plural = "Timeline Events"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_timeline_event")]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Timeline.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Inspiration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="inspirations/",
        blank=True,
        null=True,
        help_text="Upload an image related to the inspiration board (optional)",
    )
    created_by = models.ForeignKey(User, related_name="created_by_inspiration", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_inspiration", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Inspirations"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_inspiration")]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Inspiration.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField(max_length=500)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    answer = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False, help_text="Indicates if the question is viewable")
    created_by = models.ForeignKey(User, related_name="created_by_question", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_question", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.question

    class Meta:
        ordering = ["question"]
        verbose_name_plural = "Questions"
        constraints = [models.UniqueConstraint(fields=["question"], name="unique_question")]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.question[:50])
            slug = base_slug
            counter = 1

            while Question.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class WeddingSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    allow_rsvp = models.BooleanField(default=False, help_text="Enable or disable RSVP functionality")
    wedding_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "Wedding Settings"

    class Meta:
        verbose_name_plural = "Wedding Settings"

    def save(self, *args, **kwargs):  # type: ignore
        """Save object to the database. All other entries, if any, are removed."""
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> Any:
        """Load the model instance."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class RsvpFormBoolean(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    setting = models.ForeignKey(
        WeddingSettings, related_name="rsvp_form_booleans", on_delete=models.CASCADE, null=True, blank=True
    )
    question = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, related_name="created_by_rsvp_form_boolean", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_rsvp_form_boolean", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.question

    class Meta:
        ordering = ["order", "question"]
        verbose_name_plural = "RSVP Form Booleans"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.question[:50])
            slug = base_slug
            counter = 1

            while RsvpFormBoolean.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
