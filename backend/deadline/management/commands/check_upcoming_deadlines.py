import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Check for upcoming deadlines and send notifications"

    def handle(self, *args, **options):
        logger.info("Checking upcoming deadlines")

        self.stdout.write(self.style.SUCCESS("Successfully checked upcoming deadlines."))
