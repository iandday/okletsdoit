from django.contrib import admin
from .models import GuestGroup, Guest


@admin.register(GuestGroup)
class GuestGroupAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "relationship",
        "priority",
        "group_count",
        "group_invited_count",
        "group_attending_count",
        "email",
        "phone",
        "created_at",
        "is_deleted",
    ]
    list_filter = ["relationship", "priority", "is_deleted", "created_at", "updated_at"]
    search_fields = ["name", "email", "phone", "city", "state", "notes"]
    readonly_fields = [
        "id",
        "slug",
        "group_count",
        "group_invited_count",
        "group_attending_count",
        "created_at",
        "updated_at",
        "rsvp_code",
    ]
    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "rsvp_code", "relationship", "priority", "associated_with")}),
        ("Contact Information", {"fields": ("email", "phone", "address", "city", "state", "zip_code")}),
        (
            "Statistics",
            {"fields": ("group_count", "group_invited_count", "group_attending_count"), "classes": ("collapse",)},
        ),
        ("Additional Information", {"fields": ("notes",)}),
        (
            "System Information",
            {
                "fields": ("id", "created_by", "created_at", "updated_by", "updated_at", "is_deleted"),
                "classes": ("collapse",),
            },
        ),
    )
    ordering = ["name"]
    date_hierarchy = "created_at"


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "group",
        "plus_one",
        "is_invited",
        "is_attending",
        "overnight",
        "created_at",
        "is_deleted",
    ]
    list_filter = [
        "plus_one",
        "overnight",
        "is_invited",
        "is_attending",
        "is_deleted",
        "group__relationship",
        "group__priority",
        "created_at",
        "updated_at",
    ]
    search_fields = ["first_name", "last_name", "group__name", "notes", "response_notes"]
    readonly_fields = ["id", "slug", "created_at", "updated_at"]
    fieldsets = (
        ("Basic Information", {"fields": ("first_name", "last_name", "slug", "group", "plus_one", "overnight")}),
        ("RSVP Status", {"fields": ("is_invited", "is_attending")}),
        ("Notes", {"fields": ("notes", "response_notes")}),
        (
            "System Information",
            {
                "fields": ("id", "created_by", "created_at", "updated_by", "updated_at", "is_deleted"),
                "classes": ("collapse",),
            },
        ),
    )
    ordering = ["group__name", "last_name", "first_name"]
    date_hierarchy = "created_at"
    list_select_related = ["group"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("group")
