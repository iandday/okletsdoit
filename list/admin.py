from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import List
from .models import ListEntry


@admin.register(List)
class ListAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = [
        "name",
        "created_by",
        "created_at",
        "total_entries",
        "completed_entries",
        "completion_percentage",
        "is_deleted",
    ]
    list_filter = ["created_at", "updated_at", "is_deleted", "created_by"]
    search_fields = ["name", "description"]
    readonly_fields = [
        "id",
        "slug",
        "created_at",
        "updated_at",
        "total_entries",
        "completed_entries",
        "completion_percentage",
    ]
    prepopulated_fields = {}
    ordering = ["-created_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description")}),
        ("Metadata", {"fields": ("id", "created_by", "created_at", "updated_by", "updated_at")}),
        ("Status", {"fields": ("is_deleted",)}),
        (
            "Statistics",
            {"fields": ("total_entries", "completed_entries", "completion_percentage"), "classes": ("collapse",)},
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ["created_by"]
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:  # creating a new object
            obj.created_by = request.user
        else:  # updating an existing object
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ListEntry)
class ListEntryAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = [
        "item",
        "list",
        "quantity",
        "unit_price",
        "additional_price",
        "total_price",
        "is_completed",
        "completed_at",
        "purchased",
        "associated_expense",
        "created_by",
        "created_at",
        "is_deleted",
    ]
    list_filter = [
        "is_completed",
        "completed_at",
        "created_at",
        "updated_at",
        "is_deleted",
        "list",
        "created_by",
        "purchased",
        "associated_expense",
    ]
    search_fields = ["item", "description", "list__name", "associated_expense__item"]
    readonly_fields = ["id", "slug", "total_price", "created_at", "updated_at"]
    prepopulated_fields = {}
    ordering = ["list", "order", "item"]

    fieldsets = (
        ("Basic Information", {"fields": ("item", "slug", "description", "list", "order")}),
        ("Pricing", {"fields": ("quantity", "unit_price", "additional_price", "total_price")}),
        ("Expense Integration", {"fields": ("purchased", "associated_expense")}),
        ("Completion Status", {"fields": ("is_completed", "completed_at")}),
        ("Metadata", {"fields": ("id", "created_by", "created_at", "updated_by", "updated_at")}),
        ("Status", {"fields": ("is_deleted",)}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ["created_by"]
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:  # creating a new object
            obj.created_by = request.user
        else:  # updating an existing object
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
