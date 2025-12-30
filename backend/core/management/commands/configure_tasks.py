import json
import logging

from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask
import zoneinfo

logger = logging.getLogger(__name__)


tasks = [
    {
        "name": "Send planning update emails",
        "task": "core.tasks.run_management_command",
        "args": json.dumps(["send_update_email"]),
        "schedule": {
            "minute": 5,
            "hour": 3,
            "day_of_week": "0",
            "day_of_month": "*",
            "month_of_year": "*",
            "timezone": zoneinfo.ZoneInfo("UTC"),
        },
    },
]


class Command(BaseCommand):
    help = "Configure periodic tasks for the application"

    def handle(self, *args, **options):
        for task in tasks:
            schedule_data = task["schedule"]
            schedule, created = CrontabSchedule.objects.get_or_create(**schedule_data)

            periodic_task, created = PeriodicTask.objects.update_or_create(
                crontab=schedule,
                name=task["name"],
                task=task["task"],
                defaults={"args": task["args"]},
            )

            if created:
                logger.info("Created new periodic task: %s", periodic_task.name)
            else:
                logger.info("Periodic task already exists: %s", periodic_task.name)

        self.stdout.write(self.style.SUCCESS("Successfully configured periodic tasks."))
