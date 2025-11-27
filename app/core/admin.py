from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from django.db import models
from .models import Idea, RsvpQuestion, Timeline, Inspiration, Question, RsvpQuestionChoice


class RsvpQuestionChoiceInline(admin.TabularInline):
    model = RsvpQuestionChoice
    fk_name = "question"
    extra = 1
    min_num = 0
    verbose_name = "Choice"
    verbose_name_plural = "Choices"
    fields = ("choice_text",)
    show_change_link = False


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


@admin.register(RsvpQuestion)
class RsvpQuestionAdmin(admin.ModelAdmin):
    """
    Admin for RsvpQuestion. If editing an existing question of type MULTIPLE_CHOICE,
    the inline choices are shown so you can manage possible answers directly.
    """

    list_display = ("text", "question_type", "published", "order", "created_at")
    list_filter = ("question_type", "published")
    search_fields = ("text",)
    ordering = ("order", "text")
    inlines = (RsvpQuestionChoiceInline,)
    fieldsets = (
        (None, {"fields": ("text", "question_type", "order", "published")}),
        (
            "Audit",
            {
                "fields": ("created_by", "created_at", "updated_by", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    def get_inline_instances(self, request, obj=None):
        """
        Only show the choices inline when the question is (or will be) a multiple-choice question.
        When editing an existing question that is not multiple choice, hide the inline to avoid confusion.
        """
        # If editing an existing object and it's not multiple choice, don't show the choices inline.
        if obj is not None and obj.question_type != RsvpQuestion.QUESTION_TYPE_CHOICES.MULTIPLE_CHOICE:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(RsvpQuestionChoice)
class RsvpQuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question")
    search_fields = ("choice_text", "question__text")
    ordering = ("question__text", "choice_text")


admin.site.site_header = "Wedding Planning Manager"
admin.site.site_title = "Wedding Admin"
admin.site.index_title = "Manage Wedding Tasks & Ideas"
