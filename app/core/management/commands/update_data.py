from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from PIL import Image
from guestlist.models import GuestGroup


class Command(BaseCommand):
    def handle(self, *args, **options):
        # make sure every GuestGroup has an rsvp_code
        groups = GuestGroup.objects.filter(rsvp_code=None, is_deleted=False)
        for group in groups:
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Set rsvp_code for group {group.name}"))
