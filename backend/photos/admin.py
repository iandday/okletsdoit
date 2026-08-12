from django.contrib import admin
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin

from .models import UploadedPhoto


class UploadedPhotoAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "status",
        "thumbnail_preview",
        "dimensions",
        "file_size_kb",
        "camera",
        "is_approved",
        "flagged",
        "uploaded_at",
    )
    list_filter = (
        "status",
        "is_approved",
        "flagged",
        "is_deleted",
        "uploaded_at",
    )
    search_fields = (
        "id",
        "camera",
        "checksum",
        "photo_file",
    )
    ordering = ("-uploaded_at",)
    readonly_fields = (
        "id",
        "uploaded_at",
        "photo_preview",
        "thumbnail_preview",
        "photo_link",
        "thumbnail_link",
        "content_type",
        "file_size",
        "width",
        "height",
        "camera",
        "checksum",
    )

    fieldsets = (
        ("Photo", {"fields": ("status", "is_approved", "flagged", "is_deleted", "favorite_count")}),
        ("Preview", {"fields": ("thumbnail_preview", "photo_preview")}),
        ("Files", {"fields": ("photo_file", "thumbnail_file", "photo_link", "thumbnail_link")}),
        (
            "Metadata",
            {
                "fields": (
                    "content_type",
                    "file_size",
                    "width",
                    "height",
                    "camera",
                    "checksum",
                )
            },
        ),
        ("Timestamps", {"fields": ("id", "uploaded_at"), "classes": ("collapse",)}),
    )

    actions = (
        "mark_approved",
        "mark_unapproved",
        "mark_flagged",
        "mark_unflagged",
        "mark_deleted",
        "restore_deleted",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if "is_deleted__exact" in request.GET:
            return queryset
        return queryset.filter(is_deleted=False)

    @admin.display(description="Size")
    def file_size_kb(self, obj: UploadedPhoto) -> str:
        if not obj.file_size:
            return "-"
        return f"{obj.file_size / 1024:.1f} KB"

    @admin.display(description="Dimensions")
    def dimensions(self, obj: UploadedPhoto) -> str:
        if not obj.width or not obj.height:
            return "-"
        return f"{obj.width} x {obj.height}"

    @admin.display(description="Photo")
    def photo_link(self, obj: UploadedPhoto) -> str:
        if not obj.photo_file:
            return "No photo"
        return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">Open photo</a>', obj.photo_file.url)

    @admin.display(description="Thumbnail")
    def thumbnail_link(self, obj: UploadedPhoto) -> str:
        if not obj.thumbnail_file:
            return "No thumbnail"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer">Open thumbnail</a>', obj.thumbnail_file.url
        )

    @admin.display(description="Photo Preview")
    def photo_preview(self, obj: UploadedPhoto) -> str:
        if not obj.photo_file:
            return "No photo"
        return format_html(
            '<img src="{}" alt="photo" style="max-width: 360px; max-height: 360px; border-radius: 8px;" />',
            obj.photo_file.url,
        )

    @admin.display(description="Thumb")
    def thumbnail_preview(self, obj: UploadedPhoto) -> str:
        if not obj.thumbnail_file:
            return "No thumbnail"
        return format_html(
            '<img src="{}" alt="thumbnail" style="max-width: 96px; max-height: 96px; border-radius: 6px;" />',
            obj.thumbnail_file.url,
        )

    @admin.action(description="Mark selected photos as approved")
    def mark_approved(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} photo(s) marked approved.")

    @admin.action(description="Mark selected photos as unapproved")
    def mark_unapproved(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} photo(s) marked unapproved.")

    @admin.action(description="Mark selected photos as flagged")
    def mark_flagged(self, request, queryset):
        updated = queryset.update(flagged=True)
        self.message_user(request, f"{updated} photo(s) marked flagged.")

    @admin.action(description="Remove flag from selected photos")
    def mark_unflagged(self, request, queryset):
        updated = queryset.update(flagged=False)
        self.message_user(request, f"{updated} photo(s) unflagged.")

    @admin.action(description="Soft delete selected photos")
    def mark_deleted(self, request, queryset):
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f"{updated} photo(s) deleted.")

    @admin.action(description="Restore selected photos")
    def restore_deleted(self, request, queryset):
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} photo(s) restored.")


admin.site.register(UploadedPhoto, UploadedPhotoAdmin)
