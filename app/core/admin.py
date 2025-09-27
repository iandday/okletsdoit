from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from django.db import models
from .models import Idea, Timeline, Inspiration, Question


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
    list_display = ("name", "start_date", "end_date", "published", "confirmed", "is_deleted")
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

    def start_date(self, obj: Timeline):
        """Display formatted start date and time"""
        return format_html(
            '<div><strong>{}</strong><br><span class="text-xs text-base-content/50">{}</span></div>',
            obj.start.strftime("%m/%d/%Y"),
            obj.start.strftime("%I:%M %p"),
        )

    def end_date(self, obj: Timeline):
        """Display formatted end date and time"""
        if obj.end:
            return format_html(
                '<div><strong>{}</strong><br><span class="text-xs text-base-content/50">{}</span></div>',
                obj.end.strftime("%m/%d/%Y"),
                obj.end.strftime("%I:%M %p"),
            )
        else:
            return format_html('<span class="badge badge-ghost">No end</span>')

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

    actions = ["mark_as_deleted", "restore_from_deleted", "toggle_confirmed", "toggle_published"]

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

    def toggle_confirmed(self, request, queryset: models.QuerySet[Timeline]):
        """Toggle confirmation status of selected timeline events"""
        updated = queryset.update(confirmed=~models.F("confirmed"))
        self.message_user(request, f"Confirmation status of {updated} timeline events toggled.")

    toggle_confirmed.short_description = "Toggle confirmation status"

    def toggle_published(self, request, queryset):
        """Toggle published status of selected timeline events"""
        updated = queryset.update(published=~models.F("published"))
        self.message_user(request, f"Published status of {updated} timeline events toggled.")

    toggle_published.short_description = "Toggle published status"


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


@admin.register(Question)
class QuestionAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ("question", "created_by", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "is_deleted", "created_by")
    search_fields = ("question", "answer")
    prepopulated_fields = {"slug": ("question",)}
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {"fields": ("question", "slug", "answer")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted questions by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("created_by", "updated_by").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.site_header = "Wedding Planning Manager"
admin.site.site_title = "Wedding Admin"
admin.site.index_title = "Manage Wedding Tasks & Ideas"
