import datetime
import uuid

from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords
from typing import Any
from core.utils import generate_qr_code_attachment
from users.models import User
from django.conf import settings
from django.contrib.auth import get_user_model


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
    order = models.IntegerField(default=0, help_text="Display order for timeline events")
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
        ordering = ["order", "start"]
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


class QuestionCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False, help_text="Indicates if the category is viewable")
    created_by = models.ForeignKey(User, related_name="created_by_question_category", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_question_category", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_question_category")]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name[:50])
            slug = base_slug
            counter = 1

            while QuestionCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name="questions_category")
    question = models.TextField(max_length=500)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    answer = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=100, default="question-circle")
    urls = models.ManyToManyField("core.QuestionURL", blank=True, related_name="question_urls")
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
        verbose_name_plural = "FAQ Questions"
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


class QuestionURL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="questions")
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    url = models.URLField(max_length=500)
    text = models.CharField(max_length=250, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_question_url", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_question_url", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        ordering = ["url"]
        verbose_name_plural = "FAQ Question URLs"
        constraints = [models.UniqueConstraint(fields=["url"], name="unique_question_url")]

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.url[:50])
            slug = base_slug
            counter = 1

            while QuestionURL.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Tips(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name="tips_category")
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False, help_text="Indicates if the tip is viewable")
    created_by = models.ForeignKey(User, related_name="created_by_tip", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name="updated_by_tip", on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "FAQ Tips"
        constraints = [models.UniqueConstraint(fields=["content", "category"], name="unique_tip")]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.content[:50])
            slug = base_slug
            counter = 1

            while Tips.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class WeddingSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    default_data_loaded = models.BooleanField(default=False)
    show_faq = models.BooleanField(default=False, help_text="Enable or disable FAQ section on the site")
    show_venue = models.BooleanField(default=False, help_text="Enable or disable Venue section on the site")
    wedding_date = models.DateField(null=True, blank=True)
    allow_rsvp = models.BooleanField(default=False, help_text="Enable or disable RSVP functionality")
    allow_photos = models.BooleanField(default=False, help_text="Enable or disable Photo Sharing functionality")
    rsvp_default_url = models.URLField(
        max_length=500,
        default=settings.RSVP_URL,
        help_text="Default URL for RSVP page if not using personalized URLs",
    )
    rsvp_qr_code = models.ForeignKey(
        "attachments.Attachment",
        related_name="qr_code_wedding_settings",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="QR code for RSVP start page",
    )
    rsvp_qr_code_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL for RSVP start page",
    )
    rsvp_accept_button = models.TextField(default="Lets' Do This", null=True)
    rsvp_decline_button = models.TextField(default="No Thanks", null=True)
    rsvp_attending_label = models.CharField(max_length=100, default="I'll be there!")
    rsvp_accommodation_label = models.CharField(
        max_length=100, default="I'll spend the weekend at the lodge", blank=True, null=True
    )
    rsvp_vip_label = models.CharField(max_length=100, default="I'll join the VIP experience", blank=True, null=True)
    rsvp_accept_intro = models.TextField(default="We're so excited that you can make it!")
    rsvp_accept_success_message = models.TextField(default="We look forward to celebrating with you.")
    rsvp_decline_success_message = models.TextField(default="We'll miss you at the celebration.")
    rsvp_accommodation_intro = models.TextField(
        default="Please let us know if you will need accommodation during the wedding weekend.", blank=True, null=True
    )
    rsvp_vip_intro = models.TextField(
        default="Please let us know if you will be joining us for the VIP overnight experience.", blank=True, null=True
    )
    rsvp_show_accommodation_intro = models.BooleanField(default=False)
    rsvp_show_vip_intro = models.BooleanField(default=False)
    rsvp_enable_email_updates = models.BooleanField(
        default=False, help_text="Allow guests to opt-in for email updates about the wedding"
    )
    rsvp_email_update_label = models.CharField(
        max_length=150, default="Yes, keep me updated via email", blank=True, null=True
    )
    rsvp_success_headline = models.TextField(default="Thank you for your RSVP!")
    rsvp_start_date = models.DateField(null=True, blank=True)
    rsvp_end_date = models.DateField(null=True, blank=True)
    standard_group_label = models.CharField(max_length=100, default="Day")
    vip_group_label = models.CharField(max_length=100, default="Overnight")
    accommodation_group_label = models.CharField(max_length=100, default="Accommodation")
    venue_page_title = models.CharField(max_length=150, default="Our Venue")
    venue_page_description = models.TextField(
        default="Discover the beautiful location where we'll be celebrating our special day."
    )
    venue_name = models.CharField(max_length=150, default="The Lodge")
    venue_address_line_one = models.CharField(max_length=250, default="1234 Wedding Lane")
    venue_address_line_two = models.CharField(max_length=250, blank=True, null=True)
    venue_city = models.CharField(max_length=100, default="Hocking Hills")
    venue_state = models.CharField(max_length=100, default="Ohio")
    venue_zipcode = models.CharField(max_length=20, default="43119")
    venue_country = models.CharField(max_length=100, default="USA")
    venue_parking = models.TextField(blank=True, null=True)
    venue_gallery_title = models.CharField(max_length=150, default="Check Out Our Venue")
    venue_gallery_description = models.TextField(
        default="We’re really excited to celebrate with you - take a look at our venue while we wait for the big day!"
    )
    history = HistoricalRecords()

    def __str__(self):
        return "Wedding Settings"

    class Meta:
        verbose_name_plural = "Wedding Settings"

    def save(self, *args, **kwargs):  # type: ignore
        """Save object to the database. All other entries, if any, are removed."""

        # get first admin user to assign as created_by for the attachment
        User = get_user_model()
        attachment = generate_qr_code_attachment(
            url=settings.RSVP_URL,
            name="RSVP QR Code",
            model_instance=self,
            uploaded_by=User.objects.filter(is_admin=True).first(),
            filename="qr_code_base_rsvp.png",
            heart_logo=True,  # ❤️ Enable heart logo on QR codes
        )
        self.rsvp_qr_code = attachment
        self.rsvp_qr_code_url = attachment.attachment_file.url if attachment.attachment_file else ""

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


class Accommodation(models.Model):
    class ACCOMMODATION_TYPE_CHOICES(models.TextChoices):
        HOTEL = "hotel", "Hotel"
        RENTAL = "rental", "Rental"
        CAMPGROUND = "campground", "Campground"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address_line_one = models.CharField(max_length=250, blank=True, null=True)
    address_line_two = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    accommodation_type = models.CharField(
        max_length=50, choices=ACCOMMODATION_TYPE_CHOICES, default=ACCOMMODATION_TYPE_CHOICES.HOTEL
    )
    order = models.IntegerField(default=0, help_text="Display order for accommodations")
    created_by = models.ForeignKey(User, related_name="created_by_accommodation", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_accommodation", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Accommodations"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_accommodation")]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Accommodation.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
