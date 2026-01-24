from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from django.db import models
from .models import (
    Idea,
    RsvpQuestion,
    Timeline,
    Inspiration,
    RsvpQuestionChoice,
    WeddingSettings,
    Question,
    QuestionCategory,
    QuestionURL,
    Tips,
)
from .forms import FAQImportForm
from contacts.admin import ContactAdmin
from contacts.models import Contact
from deadline.admin import DeadlineListAdmin, DeadlineAdmin
from deadline.models import DeadlineList, Deadline
from expenses.admin import ExpenseAdmin
from expenses.models import Expense
from guestlist.admin import GuestAdmin, GuestGroupAdmin, RsvpSubmissionAdmin
from guestlist.models import Guest, GuestGroup, RsvpSubmission
from list.admin import ListAdmin, ListEntryAdmin
from list.models import List, ListEntry
from users.admin import UserAdmin
from users.models import User


class RsvpQuestionChoiceInline(admin.TabularInline):
    model = RsvpQuestionChoice
    fk_name = "question"
    extra = 1
    min_num = 0
    verbose_name = "Choice"
    verbose_name_plural = "Choices"
    fields = ("choice_text",)
    show_change_link = False


# class QuestionURLInline(admin.TabularInline):
#     """Inline admin for QuestionURL to manage URLs within a Question"""

#     model = QuestionURL
#     fk_name = "question"
#     extra = 1
#     min_num = 0
#     verbose_name = "Related URL"
#     verbose_name_plural = "Related URLs"
#     fields = ("url", "text")
#     show_change_link = False


# class QuestionInline(admin.StackedInline):
#     """Inline admin for Questions within a QuestionCategory"""

#     model = Question
#     fk_name = "category"
#     extra = 0
#     min_num = 0
#     verbose_name = "Question"
#     verbose_name_plural = "Questions"
#     fields = ("question", "answer", "icon", "order", "published")
#     show_change_link = True
#     classes = ("collapse",)


# class TipsInline(admin.TabularInline):
#     """Inline admin for Tips within a QuestionCategory"""

#     model = Tips
#     fk_name = "category"
#     extra = 1
#     min_num = 0
#     verbose_name = "Tip"
#     verbose_name_plural = "Tips"
#     fields = ("content", "order", "published")
#     show_change_link = False


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


class QuestionAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    """Admin for FAQ Questions"""

    list_display = ("question_preview", "category", "icon", "order", "published", "created_at")
    list_filter = ("category", "published", "created_at", "is_deleted")
    search_fields = ("question", "answer", "slug")
    prepopulated_fields = {"slug": ("question",)}
    readonly_fields = ("id", "created_at", "updated_at")
    inlines = (QuestionURLInline,)

    fieldsets = (
        ("Question Details", {"fields": ("category", "question", "slug", "answer", "icon")}),
        ("Display", {"fields": ("order", "published")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def question_preview(self, obj):
        """Display a preview of the question"""
        if len(obj.question) > 80:
            preview = obj.question[:80] + "..."
        else:
            preview = obj.question
        return format_html('<span class="text-sm">{}</span>', preview)

    question_preview.short_description = "Question"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted questions by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("category", "created_by", "updated_by").filter(is_deleted=False)

    def save_model(self, request, obj, form, change):
        """Auto-set created_by and updated_by fields"""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

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
        """Toggle published status for selected questions"""
        for obj in queryset:
            obj.published = not obj.published
            obj.save()
        self.message_user(request, f"Toggled published status for {queryset.count()} questions.")

    toggle_published.short_description = "Toggle published status"


class QuestionCategoryAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    """Admin for FAQ Categories"""

    list_display = ("name", "order", "published", "question_count", "created_at")
    list_filter = ("published", "created_at", "is_deleted")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Category Details", {"fields": ("name", "slug", "order", "published")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def question_count(self, obj):
        """Display count of questions in this category"""
        count = obj.questions_category.filter(is_deleted=False).count()
        return format_html('<span class="badge badge-primary">{}</span>', count)

    question_count.short_description = "Questions"

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
        """Toggle published status for selected categories"""
        for obj in queryset:
            obj.published = not obj.published
            obj.save()
        self.message_user(request, f"Toggled published status for {queryset.count()} categories.")

    toggle_published.short_description = "Toggle published status"


class QuestionURLAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    """Admin for Question URLs"""

    list_display = ("text", "url_preview", "question", "created_at")
    list_filter = ("created_at", "is_deleted")
    search_fields = ("url", "text", "slug")
    prepopulated_fields = {"slug": ("url",)}
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("URL Details", {"fields": ("question", "url", "text", "slug")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def url_preview(self, obj):
        """Display a clickable preview of the URL"""
        if len(obj.url) > 60:
            preview = obj.url[:60] + "..."
        else:
            preview = obj.url
        return format_html('<a href="{}" target="_blank" class="link link-primary">{}</a>', obj.url, preview)

    url_preview.short_description = "URL"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted URLs by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("question", "created_by", "updated_by").filter(is_deleted=False)

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


class TipsAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    """Admin for FAQ Tips"""

    list_display = ("content_preview", "category", "order", "published", "created_at")
    list_filter = ("category", "published", "created_at", "is_deleted")
    search_fields = ("content", "slug")
    prepopulated_fields = {"slug": ("content",)}
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Tip Details", {"fields": ("category", "content", "slug", "order", "published")}),
        ("Tracking", {"fields": ("created_by", "updated_by", "is_deleted"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def content_preview(self, obj):
        """Display a preview of the tip content"""
        if len(obj.content) > 80:
            preview = obj.content[:80] + "..."
        else:
            preview = obj.content
        return format_html('<span class="text-sm">{}</span>', preview)

    content_preview.short_description = "Content"

    def get_queryset(self, request):
        """Optimize queryset and exclude deleted tips by default"""
        queryset = super().get_queryset(request)
        return queryset.select_related("category", "created_by", "updated_by").filter(is_deleted=False)

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
        """Toggle published status for selected tips"""
        for obj in queryset:
            obj.published = not obj.published
            obj.save()
        self.message_user(request, f"Toggled published status for {queryset.count()} tips.")

    toggle_published.short_description = "Toggle published status"


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


class RsvpQuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question")
    search_fields = ("choice_text", "question__text")
    ordering = ("question__text", "choice_text")


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
            {"fields": ("wedding_date", "allow_rsvp", "allow_photos", "show_faq", "show_venue", "default_data_loaded")},
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


class DataImportAdminView(admin.AdminSite):
    """Custom admin site for importing data from Excel files"""

    site_header = "Wedding Planning Manager"
    site_title = "Wedding Admin"
    index_title = "Manage Wedding Tasks & Ideas"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("data-import/", self.admin_view(self.import_data_view), name="data_import"),
            path(
                "data-import/faq/template/",
                self.admin_view(self.download_faq_template),
                name="data_import_faq_template",
            ),
        ]
        return custom_urls + urls

    def import_data_view(self, request):
        """Main import page view"""
        if request.method == "POST":
            import_type = request.POST.get("import_type")

            if import_type == "faq":
                return self.import_faq_data(request)

            messages.error(request, "Invalid import type selected.")
            return redirect("admin:data_import")

        context = {
            "title": "Import Data from Excel",
            "site_title": self.site_title,
            "site_header": self.site_header,
            "has_permission": True,
        }
        return render(request, "admin/data_import.html", context)

    def import_faq_data(self, request):
        """Handle FAQ data import"""
        form = FAQImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            clear_existing = form.cleaned_data.get("clear_existing", False)

            import tempfile
            import os
            from django.core.management import call_command

            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                for chunk in excel_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            try:
                from io import StringIO

                out = StringIO()
                call_command(
                    "import_faq_data",
                    file=tmp_path,
                    user=request.user.email,
                    clear=clear_existing,
                    stdout=out,
                )

                messages.success(request, "FAQ data imported successfully!")
                messages.info(request, out.getvalue())

            except Exception as e:
                messages.error(request, f"Error importing FAQ data: {str(e)}")

            finally:
                os.unlink(tmp_path)

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return redirect("admin:data_import")

    def download_faq_template(self, request):
        """Generate and download FAQ Excel template"""
        from django.core.management import call_command
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp_path = tmp.name

        try:
            call_command("import_faq_data", generate_template=tmp_path)

            with open(tmp_path, "rb") as f:
                response = HttpResponse(
                    f.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                response["Content-Disposition"] = 'attachment; filename="faq_template.xlsx"'
                return response

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


custom_admin_site = DataImportAdminView(name="wedding_admin")
custom_admin_site.register(Idea, IdeaAdmin)
custom_admin_site.register(Timeline, TimelineAdmin)
custom_admin_site.register(Inspiration, InspirationAdmin)
custom_admin_site.register(RsvpQuestion, RsvpQuestionAdmin)
custom_admin_site.register(RsvpQuestionChoice, RsvpQuestionChoiceAdmin)
custom_admin_site.register(WeddingSettings, WeddingSettingsAdmin)
custom_admin_site.register(Question, QuestionAdmin)
custom_admin_site.register(QuestionCategory, QuestionCategoryAdmin)
custom_admin_site.register(QuestionURL, QuestionURLAdmin)
custom_admin_site.register(Tips, TipsAdmin)

custom_admin_site.register(Contact, ContactAdmin)
custom_admin_site.register(DeadlineList, DeadlineListAdmin)
custom_admin_site.register(Deadline, DeadlineAdmin)
custom_admin_site.register(Expense, ExpenseAdmin)
custom_admin_site.register(Guest, GuestAdmin)
custom_admin_site.register(GuestGroup, GuestGroupAdmin)
custom_admin_site.register(RsvpSubmission, RsvpSubmissionAdmin)
custom_admin_site.register(List, ListAdmin)
custom_admin_site.register(ListEntry, ListEntryAdmin)
custom_admin_site.register(User, UserAdmin)

# Replace the default admin site
admin.site = custom_admin_site
