from django.core.management.base import BaseCommand
from guestlist.models import GuestGroup


class Command(BaseCommand):
    help = "Generate missing RSVP QR codes for guest groups"

    def add_arguments(self, parser):
        parser.add_argument(
            "--regenerate",
            action="store_true",
            help="Regenerate QR codes even if they already exist",
        )

    def handle(self, *args, **options):
        regenerate = options["regenerate"]

        # Get all non-deleted guest groups
        guest_groups = GuestGroup.objects.filter(is_deleted=False)
        total_count = guest_groups.count()

        if regenerate:
            self.stdout.write(self.style.WARNING(f"Regenerating QR codes for {total_count} guest groups..."))
            generated_count = 0
            error_count = 0

            for guest_group in guest_groups:
                try:
                    # Delete existing QR code if present
                    if guest_group.qr_code:
                        old_qr = guest_group.qr_code
                        guest_group.qr_code = None
                        old_qr.is_deleted = True
                        old_qr.save()

                    # Save triggers QR code generation in model's save method
                    guest_group.save()
                    generated_count += 1

                    if generated_count % 10 == 0:
                        self.stdout.write(f"  Progress: {generated_count}/{total_count}")

                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f"  Error generating QR code for '{guest_group.name}': {str(e)}")
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully regenerated {generated_count} QR codes"
                    + (f" ({error_count} errors)" if error_count > 0 else "")
                )
            )

        else:
            # Only generate missing QR codes
            missing_qr_groups = guest_groups.filter(qr_code__isnull=True)
            missing_count = missing_qr_groups.count()

            if missing_count == 0:
                self.stdout.write(self.style.SUCCESS("All guest groups already have QR codes!"))
                return

            self.stdout.write(f"Generating QR codes for {missing_count} guest groups (out of {total_count} total)...")
            generated_count = 0
            error_count = 0

            for guest_group in missing_qr_groups:
                try:
                    # Trigger save to generate QR code
                    guest_group.save()
                    generated_count += 1

                    if generated_count % 10 == 0:
                        self.stdout.write(f"  Progress: {generated_count}/{missing_count}")

                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f"  Error generating QR code for '{guest_group.name}': {str(e)}")
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully generated {generated_count} QR codes"
                    + (f" ({error_count} errors)" if error_count > 0 else "")
                )
            )
