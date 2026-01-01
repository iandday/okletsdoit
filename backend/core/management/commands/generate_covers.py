from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from PIL import Image


class Command(BaseCommand):
    help = "Generate smaller web-friendly cover-1-small.webp and cover-2-small.webp from originals"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--max-size",
            type=int,
            default=768,
            help="Max width/height in px for the smaller images (default: 768)",
        )
        parser.add_argument(
            "--app-name",
            type=str,
            default="core",
            help="Name of the application (default: core)",
        )
        parser.add_argument(
            "--file-name",
            type=str,
            help="Name of the input file",
        )

    def handle(self, *args, **options) -> None:
        max_size: int = options["max_size"]
        app: str = options["app_name"]
        file_name = options["file_name"]
        src_file = Path(settings.BASE_DIR, app, "static", app, "img", file_name)

        if not src_file.exists():
            raise CommandError(f"Source file not found: {src_file}")

        # dest file is same path but with '-small.webp' suffix
        dest_file = src_file.with_name(src_file.stem + "-small.webp")

        dest_file.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src_file) as im:
            im = im.convert("RGB")
            im.thumbnail((max_size, max_size), Image.Resampling.BICUBIC)
            im.save(dest_file, format="WEBP", quality=85, method=6)
            self.stdout.write(self.style.SUCCESS(f"Wrote {dest_file} ({dest_file.stat().st_size / 1024:.0f} KiB)"))

        self.stdout.write(self.style.SUCCESS("Cover images generated."))
