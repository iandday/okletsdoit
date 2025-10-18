import json
import logging

from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask
import zoneinfo

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Configure periodic tasks for the application"

    def handle(self, *args, **options):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=5,
            hour=3,
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone=zoneinfo.ZoneInfo("UTC"),
        )

        task, created = PeriodicTask.objects.update_or_create(
            crontab=schedule,
            name="Check for upcoming deadlines",
            task="core.tasks.run_management_command",
            args=json.dumps(["check_upcoming_deadlines"]),
        )

        if created:
            logger.info("Created new periodic task: %s", task.name)
        else:
            logger.info("Periodic task already exists: %s", task.name)

        self.stdout.write(self.style.SUCCESS("Successfully configured periodic tasks."))
