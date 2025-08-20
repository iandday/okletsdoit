from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Idea, Timeline, Inspiration


@admin.register(Idea)
class IdeaAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ("name", "created_by", "description_preview", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "is_deleted", "created_by")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def description_preview(self, obj):
        """Display a preview of the description"""
        if obj.description:
            # Strip HTML tags for preview
            import re

            plain_text = re.sub(r"<[^>]+>", "", obj.description)
            if len(plain_text) > 100:
                preview = plain_text[:100] + "..."
            else:
                preview = plain_text
            return format_html('<span class="text-sm text-base-content/70">{}</span>', preview)
        return format_html('<span class="badge badge-ghost">No description</span>')

    description_preview.short_description = "Description"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted ideas by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("created_by", "updated_by").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    actions = ["mark_as_deleted", "restore_from_deleted"]

    def mark_as_deleted(self, request, queryset):
        """Mark selected ideas as deleted"""
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f"{updated} ideas marked as deleted.")

    mark_as_deleted.short_description = "Mark selected ideas as deleted"

    def restore_from_deleted(self, request, queryset):
        """Restore selected ideas from deleted"""
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} ideas restored from deleted.")

    restore_from_deleted.short_description = "Restore selected ideas from deleted"


@admin.register(Timeline)
class TimelineAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ("name", "start_date", "end_date", "status_badges", "created_by", "created_at", "updated_at")
    list_filter = ("start", "end", "published", "confirmed", "is_deleted", "created_by")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description")}),
        ("Schedule", {"fields": ("start", "end")}),
        ("Status", {"fields": ("published", "confirmed")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def start_date(self, obj):
        """Display formatted start date and time"""
        return format_html(
            '<div><strong>{}</strong><br><span class="text-xs text-base-content/50">{}</span></div>',
            obj.start.strftime("%m/%d/%Y"),
            obj.start.strftime("%I:%M %p"),
        )

    start_date.short_description = "Start"

    def end_date(self, obj):
        """Display formatted end date and time"""
        return format_html(
            '<div><strong>{}</strong><br><span class="text-xs text-base-content/50">{}</span></div>',
            obj.end.strftime("%m/%d/%Y"),
            obj.end.strftime("%I:%M %p"),
        )

    end_date.short_description = "End"

    def status_badges(self, obj):
        """Display status badges for confirmation and publication"""
        confirmed_badge = (
            '<span class="badge badge-success">Confirmed</span>'
            if obj.confirmed
            else '<span class="badge badge-warning">Pending</span>'
        )
        published_badge = (
            '<span class="badge badge-accent">Published</span>'
            if obj.published
            else '<span class="badge badge-ghost">Draft</span>'
        )
        return format_html("{} {}", confirmed_badge, published_badge)

    status_badges.short_description = "Status"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted timeline events by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("created_by", "updated_by").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    actions = ["mark_as_deleted", "restore_from_deleted", "mark_as_confirmed", "mark_as_published"]

    def mark_as_deleted(self, request, queryset):
        """Mark selected timeline events as deleted"""
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f"{updated} timeline events marked as deleted.")

    mark_as_deleted.short_description = "Mark selected events as deleted"

    def restore_from_deleted(self, request, queryset):
        """Restore selected timeline events from deleted"""
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} timeline events restored from deleted.")

    restore_from_deleted.short_description = "Restore selected events from deleted"

    def mark_as_confirmed(self, request, queryset):
        """Mark selected timeline events as confirmed"""
        updated = queryset.update(confirmed=True)
        self.message_user(request, f"{updated} timeline events marked as confirmed.")

    mark_as_confirmed.short_description = "Mark selected events as confirmed"

    def mark_as_published(self, request, queryset):
        """Mark selected timeline events as published"""
        updated = queryset.update(published=True)
        self.message_user(request, f"{updated} timeline events marked as published.")

    mark_as_published.short_description = "Mark selected events as published"


@admin.register(Inspiration)
class InspirationAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ("name", "created_by", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "is_deleted", "created_by")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description", "image")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted inspirations by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("created_by", "updated_by").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# Custom admin site configuration for better styling with daisyUI 5
admin.site.site_header = "Wedding Planning Manager"
admin.site.site_title = "Wedding Admin"
admin.site.index_title = "Manage Wedding Tasks & Ideas"
