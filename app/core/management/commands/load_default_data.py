from __future__ import annotations

from django.core.management.base import BaseCommand
from core.models import RsvpQuestion, RsvpQuestionChoice, WeddingSettings
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

            questions = [
                {"type": "text", "text": "Do you have any food allergies or dietary restrictions?"},
                {"type": "text", "text": "Do you have any accessibility requirements we should be aware of?"},
                {"type": "text", "text": "Wedding planning is hard—can you tell us a joke?"},
                {
                    "type": "multiple_choice",
                    "text": "Will you be attending the wedding ceremony?",
                    "choices": ["Yes", "No"],
                },
                {
                    "type": "multiple_choice",
                    "text": "Will you be attending the wedding reception?",
                    "choices": ["Yes", "No"],
                },
            ]

            for idx, question in enumerate(questions, start=1):
                if question["type"] == "text":
                    RsvpQuestion.objects.update_or_create(
                        text=question["text"],
                        defaults={
                            "order": idx,
                            "question_type": RsvpQuestion.QUESTION_TYPE_CHOICES.TEXT,
                            "published": True,
                            "created_by": admin_user,
                        },
                    )
                elif question["type"] == "multiple_choice":
                    q, _ = RsvpQuestion.objects.update_or_create(
                        text=question["text"],
                        defaults={
                            "order": idx,
                            "question_type": RsvpQuestion.QUESTION_TYPE_CHOICES.MULTIPLE_CHOICE,
                            "published": True,
                            "created_by": admin_user,
                        },
                    )
                    for choice in question["choices"]:
                        RsvpQuestionChoice.objects.update_or_create(
                            question=q,
                            choice_text=choice,
                        )

            settings.default_data_loaded = True
            settings.save()
            self.stdout.write(self.style.SUCCESS("Default wedding settings data loaded."))
        else:
            self.stdout.write("Default wedding settings data already loaded. Use --force to reload.")
