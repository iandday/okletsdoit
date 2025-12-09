from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import DeadlineList, Deadline


@admin.register(DeadlineList)
class DeadlineListAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ("name", "slug", "created_by", "created_at", "updated_by", "updated_at", "is_deleted")
    search_fields = ("name", "slug")
    list_filter = ("is_deleted", "created_by", "updated_by")
    readonly_fields = ("created_at", "updated_at", "slug")
    ordering = ("name",)


@admin.register(Deadline)
class DeadlineAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = (
        "name",
        "slug",
        "deadline_list",
        "due_date",
        "assigned_to",
        "completed",
        "completed_at",
        "is_deleted",
    )
    search_fields = ("name", "slug", "description")
    list_filter = ("completed", "is_deleted", "deadline_list", "assigned_to")
    readonly_fields = ("created_at", "updated_at", "slug", "completed_at")
    ordering = ("due_date", "created_at")
