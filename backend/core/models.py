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
    default_data_loaded = models.BooleanField(default=False)
    show_faq = models.BooleanField(default=False, help_text="Enable or disable FAQ section on the site")
    wedding_date = models.DateField(null=True, blank=True)
    allow_rsvp = models.BooleanField(default=False, help_text="Enable or disable RSVP functionality")
    allow_photos = models.BooleanField(default=False, help_text="Enable or disable Photo Sharing functionality")
    rsvp_accept_button = models.TextField(default="Lets' Do This", null=True)
    rsvp_decline_button = models.TextField(default="No Thanks", null=True)
    rsvp_attending_label = models.CharField(max_length=100, default="I'll be there!")
    rsvp_accommodation_label = models.CharField(max_length=100, default="I'll spend the weekend at the lodge")
    rsvp_vip_label = models.CharField(max_length=100, default="I'll join the VIP experience")
    rsvp_accept_intro = models.TextField(default="We're so excited that you can make it!")
    rsvp_accept_success_message = models.TextField(default="We look forward to celebrating with you.")
    rsvp_decline_success_message = models.TextField(default="We'll miss you at the celebration.")
    rsvp_accommodation_intro = models.TextField(
        default="Please let us know if you will need accommodation during the wedding weekend."
    )
    rsvp_vip_intro = models.TextField(
        default="Please let us know if you will be joining us for the VIP overnight experience."
    )
    rsvp_show_accommodation_intro = models.BooleanField(default=False)
    rsvp_show_vip_intro = models.BooleanField(default=False)
    rsvp_enable_email_updates = models.BooleanField(
        default=False, help_text="Allow guests to opt-in for email updates about the wedding"
    )
    rsvp_email_update_label = models.CharField(max_length=150, default="Yes, keep me updated via email")
    rsvp_success_headline = models.TextField(default="Thank you for your RSVP!")
    rsvp_start_date = models.DateField(null=True, blank=True)
    rsvp_end_date = models.DateField(null=True, blank=True)
    standard_group_label = models.CharField(max_length=100, default="Day")
    vip_group_label = models.CharField(max_length=100, default="Overnight")
    history = HistoricalRecords()

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


class RsvpQuestion(models.Model):
    class QUESTION_TYPE_CHOICES(models.TextChoices):
        TEXT = "text", "Text Response"
        YES_NO = "yes_no", "Yes/No"
        SINGLE_CHOICE = "single_choice", "Single Choice"
        MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False, help_text="Indicates if the question is viewable")
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    created_by = models.ForeignKey(User, related_name="created_by_rsvp_question", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_rsvp_question", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["text"]
        verbose_name_plural = "RSVP Questions"
        constraints = [models.UniqueConstraint(fields=["text"], name="unique_rsvp_question")]


class RsvpQuestionChoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(RsvpQuestion, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, related_name="created_by_rsvp_question_choice", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_rsvp_question_choice", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.choice_text
