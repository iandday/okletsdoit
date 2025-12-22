from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from django.db import models
from .models import (
    Idea,
    RsvpQuestion,
    Timeline,
    Inspiration,
    Question,
    QuestionCategory,
    QuestionURL,
    Tips,
    RsvpQuestionChoice,
    WeddingSettings,
)


class RsvpQuestionChoiceInline(admin.TabularInline):
    model = RsvpQuestionChoice
    fk_name = "question"
    extra = 1
    min_num = 0
    verbose_name = "Choice"
    verbose_name_plural = "Choices"
    fields = ("choice_text",)
    show_change_link = False


class QuestionURLInline(admin.TabularInline):
    """Inline admin for QuestionURL to manage URLs within a Question"""

    model = QuestionURL
    fk_name = "question"
    extra = 1
    min_num = 0
    verbose_name = "Related URL"
    verbose_name_plural = "Related URLs"
    fields = ("url", "text")
    show_change_link = False


class QuestionInline(admin.StackedInline):
    """Inline admin for Questions within a QuestionCategory"""

    model = Question
    fk_name = "category"
    extra = 0
    min_num = 0
    verbose_name = "Question"
    verbose_name_plural = "Questions"
    fields = ("question", "answer", "icon", "order", "published")
    show_change_link = True
    classes = ("collapse",)


class TipsInline(admin.TabularInline):
    """Inline admin for Tips within a QuestionCategory"""

    model = Tips
    fk_name = "category"
    extra = 1
    min_num = 0
    verbose_name = "Tip"
    verbose_name_plural = "Tips"
    fields = ("content", "order", "published")
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


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    """
    Admin for QuestionCategory with inline management of Questions, QuestionURLs, and Tips.
    This provides a single view to manage all FAQ-related content.
    """

    list_display = ("name", "order", "published", "question_count", "tip_count", "created_at")
    list_filter = ("published", "created_at", "updated_at", "is_deleted", "created_by")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("order", "name")
    inlines = [QuestionInline, TipsInline]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "order", "published")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def question_count(self, obj):
        """Display count of questions in this category"""
        count = obj.questions_category.filter(is_deleted=False).count()
        if count > 0:
            return format_html('<span class="badge badge-primary">{}</span>', count)
        return format_html('<span class="badge badge-ghost">0</span>')

    question_count.short_description = "Questions"

    def tip_count(self, obj):
        """Display count of tips in this category"""
        count = obj.tips_category.filter(is_deleted=False).count()
        if count > 0:
            return format_html('<span class="badge badge-accent">{}</span>', count)
        return format_html('<span class="badge badge-ghost">0</span>')

    tip_count.short_description = "Tips"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted categories by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("created_by", "updated_by").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """Auto-set created_by and updated_by for inline models"""
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.created_by_id:  # New instance (no created_by set yet)
                instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()
        # Handle deleted objects
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()

    actions = ["mark_as_deleted", "restore_from_deleted", "toggle_published"]

    def mark_as_deleted(self, request, queryset):
        """Mark selected categories as deleted"""
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f"{updated} categories marked as deleted.")

    mark_as_deleted.short_description = "Mark selected categories as deleted"

    def restore_from_deleted(self, request, queryset):
        """Restore selected categories from deleted"""
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} categories restored from deleted.")

    restore_from_deleted.short_description = "Restore selected categories from deleted"

    def toggle_published(self, request, queryset):
        """Toggle published status of selected categories"""
        updated = queryset.update(published=~models.F("published"))
        self.message_user(request, f"Published status of {updated} categories toggled.")

    toggle_published.short_description = "Toggle published status"


@admin.register(Question)
class QuestionAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    """
    Admin for individual Questions with URL management.
    Can also be managed through QuestionCategory admin.
    """

    list_display = ("question_preview", "category", "published", "order", "icon", "url_count", "created_at")
    list_filter = ("category", "published", "created_at", "updated_at", "is_deleted", "created_by")
    search_fields = ("question", "answer", "slug")
    prepopulated_fields = {"slug": ("question",)}
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("category", "order", "question")
    inlines = [QuestionURLInline]

    fieldsets = (
        ("Basic Information", {"fields": ("category", "question", "slug", "answer", "icon")}),
        ("Display Settings", {"fields": ("order", "published")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def question_preview(self, obj):
        """Display a preview of the question"""
        if len(obj.question) > 50:
            preview = obj.question[:50] + "..."
        else:
            preview = obj.question
        return format_html("<span>{}</span>", preview)

    question_preview.short_description = "Question"

    def url_count(self, obj):
        """Display count of URLs for this question"""
        count = obj.questions.filter(is_deleted=False).count()
        if count > 0:
            return format_html('<span class="badge badge-info">{}</span>', count)
        return format_html('<span class="badge badge-ghost">0</span>')

    url_count.short_description = "URLs"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted questions by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("created_by", "updated_by", "category").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """Auto-set created_by and updated_by for inline URLs"""
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.created_by_id:  # New instance (no created_by set yet)
                instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()
        # Handle deleted objects
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()

    actions = ["mark_as_deleted", "restore_from_deleted", "toggle_published"]

    def mark_as_deleted(self, request, queryset):
        """Mark selected questions as deleted"""
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f"{updated} questions marked as deleted.")

    mark_as_deleted.short_description = "Mark selected questions as deleted"

    def restore_from_deleted(self, request, queryset):
        """Restore selected questions from deleted"""
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} questions restored from deleted.")

    restore_from_deleted.short_description = "Restore selected questions from deleted"

    def toggle_published(self, request, queryset):
        """Toggle published status of selected questions"""
        updated = queryset.update(published=~models.F("published"))
        self.message_user(request, f"Published status of {updated} questions toggled.")

    toggle_published.short_description = "Toggle published status"


@admin.register(QuestionURL)
class QuestionURLAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    """Admin for individual QuestionURLs - can also be managed through Question admin"""

    list_display = ("url_preview", "text", "question", "created_at")
    list_filter = ("created_at", "updated_at", "is_deleted", "created_by")
    search_fields = ("url", "text", "question__question")
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {"fields": ("question", "url", "text")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def url_preview(self, obj):
        """Display a preview of the URL"""
        if len(obj.url) > 50:
            preview = obj.url[:50] + "..."
        else:
            preview = obj.url
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, preview)

    url_preview.short_description = "URL"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted URLs by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("created_by", "updated_by", "question").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    actions = ["mark_as_deleted", "restore_from_deleted"]

    def mark_as_deleted(self, request, queryset):
        """Mark selected URLs as deleted"""
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f"{updated} URLs marked as deleted.")

    mark_as_deleted.short_description = "Mark selected URLs as deleted"

    def restore_from_deleted(self, request, queryset):
        """Restore selected URLs from deleted"""
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} URLs restored from deleted.")

    restore_from_deleted.short_description = "Restore selected URLs from deleted"


@admin.register(Tips)
class TipsAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    """Admin for individual Tips - can also be managed through QuestionCategory admin"""

    list_display = ("content_preview", "category", "published", "order", "created_at")
    list_filter = ("category", "published", "created_at", "updated_at", "is_deleted", "created_by")
    search_fields = ("content", "slug")
    prepopulated_fields = {"slug": ("content",)}
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("category", "order")

    fieldsets = (
        ("Basic Information", {"fields": ("category", "content", "slug")}),
        ("Display Settings", {"fields": ("order", "published")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def content_preview(self, obj):
        """Display a preview of the tip content"""
        if len(obj.content) > 100:
            preview = obj.content[:100] + "..."
        else:
            preview = obj.content
        return format_html("<span>{}</span>", preview)

    content_preview.short_description = "Content"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted tips by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("created_by", "updated_by", "category").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    actions = ["mark_as_deleted", "restore_from_deleted", "toggle_published"]

    def mark_as_deleted(self, request, queryset):
        """Mark selected tips as deleted"""
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f"{updated} tips marked as deleted.")

    mark_as_deleted.short_description = "Mark selected tips as deleted"

    def restore_from_deleted(self, request, queryset):
        """Restore selected tips from deleted"""
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} tips restored from deleted.")

    restore_from_deleted.short_description = "Restore selected tips from deleted"

    def toggle_published(self, request, queryset):
        """Toggle published status of selected tips"""
        updated = queryset.update(published=~models.F("published"))
        self.message_user(request, f"Published status of {updated} tips toggled.")

    toggle_published.short_description = "Toggle published status"


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


@admin.register(WeddingSettings)
class WeddingSettingsAdmin(SimpleHistoryAdmin):
    """
    Admin for WeddingSettings singleton model.
    Only one instance can exist, so we disable add/delete actions.
    """

    list_display = ("__str__", "wedding_date", "allow_rsvp")
    readonly_fields = ("id",)

    fieldsets = (
        (
            "General Settings",
            {"fields": ("wedding_date", "allow_rsvp", "allow_photos", "show_faq", "default_data_loaded")},
        ),
        (
            "RSVP Button Text",
            {
                "fields": ("rsvp_accept_button", "rsvp_decline_button"),
                "classes": ("collapse",),
            },
        ),
        (
            "RSVP Labels",
            {
                "fields": (
                    "rsvp_attending_label",
                    "rsvp_accommodation_label",
                    "rsvp_vip_label",
                    "standard_group_label",
                    "vip_group_label",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "RSVP Messages",
            {
                "fields": (
                    "rsvp_accept_intro",
                    "rsvp_accept_success_message",
                    "rsvp_decline_success_message",
                    "rsvp_accommodation_intro",
                    "rsvp_vip_intro",
                    "rsvp_success_headline",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "RSVP Display Options",
            {
                "fields": (
                    "rsvp_show_accommodation_intro",
                    "rsvp_show_vip_intro",
                    "rsvp_enable_email_updates",
                    "rsvp_email_update_label",
                ),
                "classes": ("collapse",),
            },
        ),
        ("System", {"fields": ("id",), "classes": ("collapse",)}),
    )

    def has_add_permission(self, request):
        """Prevent adding new instances - singleton pattern"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton instance"""
        return False


admin.site.site_header = "Wedding Planning Manager"
admin.site.site_title = "Wedding Admin"
admin.site.index_title = "Manage Wedding Tasks & Ideas"
