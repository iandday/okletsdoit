from django.contrib import admin

from core.models import RsvpQuestion

from .models import GuestGroup, Guest, RsvpSubmission, RsvpQuestionResponse


class RsvpQuestionResponseInline(admin.TabularInline):
    model = RsvpQuestionResponse
    fk_name = "submission"
    extra = 0
    fields = ("question_display", "response")
    readonly_fields = ("question_display", "response")
    show_change_link = False

    def question_display(self, obj: RsvpQuestionResponse):
        return obj.question.text

    def response(self, obj: RsvpQuestionResponse):
        if obj.question.question_type == RsvpQuestion.QUESTION_TYPE_CHOICES.TEXT:
            return obj.response_text
        else:
            return ", ".join(c.choice_text for c in obj.response_choices.all())

    question_display.short_description = "Question"  # pyright: ignore[reportFunctionMemberAccess]
    response.short_description = "Response"  # pyright: ignore[reportFunctionMemberAccess]


@admin.register(RsvpSubmission)
class RsvpSubmissionAdmin(admin.ModelAdmin):
    list_display = ("guest_group", "created_at", "email_updates", "email_address")
    list_filter = ("email_updates",)
    search_fields = ("guest_group__name", "email_address")
    inlines = (RsvpQuestionResponseInline,)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("guest_group").prefetch_related(
            "question_responses__question",
            "question_responses__response_choices",
        )


@admin.register(GuestGroup)
class GuestGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "rsvp_code", "group_count", "group_attending_count")
    search_fields = ("name", "rsvp_code")


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "group", "is_invited", "is_attending")
    search_fields = ("first_name", "last_name", "group__name")
