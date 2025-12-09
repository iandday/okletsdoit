from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = [
        "name",
        "company",
        "email",
        "phone",
        "category",
        "created_by",
        "created_at",
        "is_deleted",
    ]
    list_filter = ["category", "created_at", "updated_at", "is_deleted", "created_by"]
    search_fields = ["name", "company", "email", "phone", "category", "notes"]
    readonly_fields = [
        "id",
        "slug",
        "created_at",
        "updated_at",
        "files_list",
    ]
    prepopulated_fields = {}
    ordering = ["name", "company"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "company", "category")}),
        ("Contact Details", {"fields": ("email", "phone", "website")}),
        ("Notes", {"fields": ("notes",)}),
        ("Files", {"fields": ("files_list",)}),
        ("Metadata", {"fields": ("id", "created_by", "created_at", "updated_by", "updated_at")}),
        ("Status", {"fields": ("is_deleted",)}),
    )

    def files_list(self, obj):
        files = obj.files.all()
        if not files:
            return "No files uploaded"
        return format_html(
            "<br>".join(
                [f'<a href="{file.file.url}" target="_blank">{file.name or file.file.name}</a>' for file in files]
            )
        )

    def save_model(self, request, obj, form, change):
        if not change:  # creating a new object
            obj.created_by = request.user
        else:  # updating an existing object
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
