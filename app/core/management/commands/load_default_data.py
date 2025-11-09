from __future__ import annotations

from django.core.management.base import BaseCommand
from core.models import RsvpFormBoolean, WeddingSettings, RsvpFormInput
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force reload of default data even if already loaded",
        )

    def handle(self, *args, **options):
        # create default wedding settings if none exist
        if not WeddingSettings.objects.first():
            settings = WeddingSettings.objects.create(wedding_date=None)
        else:
            settings = WeddingSettings.objects.first()

        if settings and (not settings.default_data_loaded or options["force"]):
            # find first admin user to assign as created_by
            User = get_user_model()
            admin_user = User.objects.filter(is_admin=True).first()

            default_boolean_questions = [
                {
                    "question": "Do you want to receive email updates about the wedding?",
                    "description": "Opt-in to receive email updates and announcements regarding the wedding.",
                },
            ]

            default_input_questions = [
                {
                    "question": "Email Address",
                    "description": "Where should we send wedding-related emails?",
                },
            ]
            for question in default_boolean_questions:
                RsvpFormBoolean.objects.get_or_create(
                    question=question["question"],
                    description=question["description"],
                    setting=settings,
                    created_by=admin_user,
                )

            for question in default_input_questions:
                RsvpFormInput.objects.get_or_create(
                    question=question["question"],
                    description=question["description"],
                    setting=settings,
                    created_by=admin_user,
                )

            settings.default_data_loaded = True
            settings.save()
            self.stdout.write(self.style.SUCCESS("Default wedding settings data loaded."))
        else:
            self.stdout.write("Default wedding settings data already loaded. Use --force to reload.")
