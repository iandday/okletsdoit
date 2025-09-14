from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from attachments.admin import AttachmentInlines

from .models import Category
from .models import Expense


@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ("name", "slug", "created_by", "created_at", "is_deleted")
    list_filter = ("is_deleted", "created_at", "updated_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "updated_at")
    list_per_page = 25
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "slug", "description")}),
        (
            "Meta Information",
            {
                "fields": ("id", "created_by", "updated_by", "created_at", "updated_at", "is_deleted"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Expense)
class ExpenseAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    inlines = (AttachmentInlines,)
    list_display = (
        "item",
        "category",
        "date",
        "estimated_amount",
        "actual_amount",
        "created_by",
        "is_deleted",
        "updated_by",
    )
    list_filter = ("category", "is_deleted", "date", "created_at")
    search_fields = ("item", "description", "category__name")
    prepopulated_fields = {"slug": ("item",)}
    readonly_fields = ("id", "created_at", "updated_at")
    list_per_page = 25
    date_hierarchy = "date"
    ordering = ("-date", "item")

    fieldsets = (
        (None, {"fields": ("item", "slug", "description", "date", "category")}),
        (
            "Financial Information",
            {
                "fields": ("estimated_amount", "actual_amount"),
            },
        ),
        (
            "Meta Information",
            {
                "fields": ("id", "created_by", "updated_by", "created_at", "updated_at", "is_deleted"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
