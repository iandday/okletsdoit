from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Task, TaskList, Idea


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "task_count", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "is_deleted")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def task_count(self, obj):
        """Display the number of tasks in this list"""
        count = obj.task_set.count()
        if count > 0:
            url = reverse("admin:core_task_changelist") + f"?task_list__id__exact={obj.id}"
            return format_html('<a href="{}" class="btn btn-sm btn-outline">{} tasks</a>', url, count)
        return f"{count} tasks"

    task_count.short_description = "Tasks"
    task_count.admin_order_field = "task_count"

    def get_queryset(self, request):
        """Optimize queryset with task count"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("task_set").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_list", "assigned_to", "priority", "due_date_display", "status_display", "created_at")
    list_filter = ("completed", "task_list", "priority", "due_date", "created_at", "assigned_to", "is_deleted")
    search_fields = ("title", "description", "slug")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("id", "created_at", "updated_at", "completed_at", "overdue_status")
    date_hierarchy = "due_date"

    fieldsets = (
        ("Task Details", {"fields": ("title", "slug", "description", "task_list")}),
        ("Assignment & Priority", {"fields": ("assigned_to", "priority", "due_date")}),
        ("Status", {"fields": ("completed", "completed_note"), "classes": ("collapse",)}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        (
            "Timestamps",
            {"fields": ("id", "created_at", "updated_at", "completed_at", "overdue_status"), "classes": ("collapse",)},
        ),
    )

    def due_date_display(self, obj):
        """Display due date with status styling"""
        if not obj.due_date:
            return format_html('<span class="badge badge-ghost">No due date</span>')

        if obj.completed:
            return format_html('<span class="badge badge-success">{}</span>', obj.due_date.strftime("%Y-%m-%d"))
        elif obj.overdue_status():
            return format_html('<span class="badge badge-error">{} (Overdue)</span>', obj.due_date.strftime("%Y-%m-%d"))
        else:
            return format_html('<span class="badge badge-info">{}</span>', obj.due_date.strftime("%Y-%m-%d"))

    due_date_display.short_description = "Due Date"
    due_date_display.admin_order_field = "due_date"

    def status_display(self, obj):
        """Display task status with badges"""
        if obj.completed:
            return format_html('<span class="badge badge-success">✓ Completed</span>')
        elif obj.overdue_status():
            return format_html('<span class="badge badge-error">⚠ Overdue</span>')
        else:
            return format_html('<span class="badge badge-warning">📋 Pending</span>')

    status_display.short_description = "Status"
    status_display.admin_order_field = "completed"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted tasks by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("task_list", "assigned_to", "created_by").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    actions = ["mark_completed", "mark_pending"]

    def mark_completed(self, request, queryset):
        """Mark selected tasks as completed"""
        updated = queryset.update(completed=True)
        self.message_user(request, f"{updated} tasks marked as completed.")

    mark_completed.short_description = "Mark selected tasks as completed"

    def mark_pending(self, request, queryset):
        """Mark selected tasks as pending"""
        updated = queryset.update(completed=False, completed_at=None)
        self.message_user(request, f"{updated} tasks marked as pending.")

    mark_pending.short_description = "Mark selected tasks as pending"


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
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


# Custom admin site configuration for better styling with daisyUI 5
admin.site.site_header = "Wedding Planning Manager"
admin.site.site_title = "Wedding Admin"
admin.site.index_title = "Manage Wedding Tasks & Ideas"
