from django.contrib import admin

from .models import GuestGroup, Guest, RsvpSubmission


@admin.register(RsvpSubmission)
class RsvpSubmissionAdmin(admin.ModelAdmin):
    list_display = ("guest_group", "created_at", "email_updates", "email_address")
    list_filter = ("email_updates",)
    search_fields = ("guest_group__name", "email_address")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    # def get_queryset(self, request):
    #    qs = super().get_queryset(request)
    #    return qs.select_related("guest_group").prefetch_related("boolean_answers__question", "input_answers__question")


@admin.register(GuestGroup)
class GuestGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "rsvp_code", "group_count", "group_attending_count")
    search_fields = ("name", "rsvp_code")


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "group", "is_invited", "is_attending")
    search_fields = ("first_name", "last_name", "group__name")
