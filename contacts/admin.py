from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
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
    ]
    prepopulated_fields = {}
    ordering = ["name", "company"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "company", "category")}),
        ("Contact Details", {"fields": ("email", "phone", "website")}),
        ("Notes", {"fields": ("notes",)}),
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
