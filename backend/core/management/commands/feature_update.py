from __future__ import annotations

from django.core.management.base import BaseCommand
from guestlist.models import Guest
from django.utils.text import slugify
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        for guest in Guest.objects.filter(overnight=True, is_deleted=False):
            guest.vip = True
            guest.save()

        for guest in Guest.objects.filter(Q(first_name="None") | Q(last_name="None"), is_deleted=False):
            guest.first_name = "Guest"
            guest.last_name = "Guest"
            base_slug = slugify(f"{guest.first_name}_{guest.last_name}")
            slug = base_slug
            counter = 1

            while Guest.objects.filter(slug=slug).exclude(pk=guest.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            guest.slug = slug
            guest.save()

        for guest in Guest.objects.filter(overnight=True, is_deleted=False):
            guest.overnight = False
            guest.save()
