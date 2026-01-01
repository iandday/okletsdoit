import uuid
from django.db import models
from django_stubs_ext.db.models.manager import RelatedManager
from simple_history.models import HistoricalRecords
from django.utils.text import slugify
from core.models import RsvpQuestion, RsvpQuestionChoice
from users.models import User


class GuestGroup(models.Model):
    class RELATIONSHIP_CHOICES(models.TextChoices):
        RELATIVE = "Rel", "Relative"
        FRIEND = "Fri", "Friend"
        COLLEAGUE = "Col", "Colleague"

    class PRIORITY_CHOICES(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100)
    address_name = models.CharField(max_length=250, blank=True)
    notes = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    address_two = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    relationship = models.CharField(
        max_length=3, choices=RELATIONSHIP_CHOICES.choices, default=RELATIONSHIP_CHOICES.RELATIVE
    )
    priority = models.IntegerField(choices=PRIORITY_CHOICES.choices, default=PRIORITY_CHOICES.MEDIUM)
    associated_with = models.ForeignKey(
        User, related_name="associated_with_guest_group", on_delete=models.CASCADE, null=True, blank=True
    )
    rsvp_code = models.CharField(max_length=10, null=True, help_text="Unique code for RSVP tracking")
    created_by = models.ForeignKey(User, related_name="created_by_guest_group", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_guest_group", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()
    guests: RelatedManager["Guest"] = None  # Type hint for the reverse relation

    def __str__(self):
        return self.name

    @property
    def group_count(self):
        return self.guests.filter(is_deleted=False).count()

    @property
    def group_standard(self):
        return self.guests.filter(vip=False, is_deleted=False).count()

    @property
    def group_vip(self):
        return self.guests.filter(vip=True, is_deleted=False).count()

    @property
    def group_overnight(self):
        return self.guests.filter(accommodation=True, is_deleted=False).count()

    @property
    def group_invited_count(self):
        return self.guests.filter(is_invited=True, is_deleted=False).count()

    @property
    def group_attending_count(self):
        return self.guests.filter(is_attending=True, is_deleted=False).count()

    @property
    def group_declined_count(self):
        return self.guests.filter(is_attending=False, responded=True, is_deleted=False).count()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while GuestGroup.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        # generate rsvp code if not set
        if not self.rsvp_code:
            rsvp_code = uuid.uuid4().hex[:10].upper()
            while GuestGroup.objects.filter(rsvp_code=rsvp_code).exists():
                rsvp_code = uuid.uuid4().hex[:10].upper()
            self.rsvp_code = rsvp_code

        super().save(*args, **kwargs)


class Guest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=50, default="Guest")
    last_name = models.CharField(max_length=50, default="Guest")
    plus_one = models.BooleanField(default=False, help_text="Indicates if this guest is a plus one of another guest")
    group = models.ForeignKey(GuestGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="guests")
    is_invited = models.BooleanField(default=False)
    is_attending = models.BooleanField(default=False)
    responded = models.BooleanField(default=False, help_text="Indicates if this guest has responded to the invitation")
    accept_accommodation = models.BooleanField(default=False, help_text="Indicates if this guest accepts accommodation")
    accept_vip = models.BooleanField(default=False, help_text="Indicates if this guest accepts VIP status")
    accommodation = models.BooleanField(
        default=False, help_text="Indicates if this guest will use overnight accommodation"
    )
    vip = models.BooleanField(default=False, help_text="Indicates if this guest is a VIP")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name="created_by_guest", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_guest", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_name}_{self.last_name}")
            slug = base_slug
            counter = 1

            while Guest.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class RsvpSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest_group = models.ForeignKey(GuestGroup, on_delete=models.CASCADE, related_name="rsvp_submissions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_updates = models.BooleanField(default=False)
    email_address = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords()

    @property
    def accept_accommodation_count(self):
        return self.guest_group.guests.filter(responded=True, accept_accommodation=True, is_deleted=False).count()

    @property
    def accept_vip_count(self):
        return self.guest_group.guests.filter(responded=True, accept_vip=True, is_deleted=False).count()

    class Meta:
        unique_together = ("guest_group",)


class RsvpQuestionResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(RsvpSubmission, related_name="question_responses", on_delete=models.CASCADE)
    question = models.ForeignKey(RsvpQuestion, related_name="responses", on_delete=models.CASCADE)
    response_text = models.TextField(blank=True, null=True)
    response_choices = models.ManyToManyField(
        RsvpQuestionChoice,
        blank=True,
        related_name="responses",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("submission", "question")

    def __str__(self):
        return f"Response to {self.question} for submission {self.submission}"
