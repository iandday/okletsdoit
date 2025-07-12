from django.contrib.auth import get_user_model
from expenses.models import Category
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Populate the Category model with default wedding expense categories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-email",
            type=str,
            help="Email of the user to set as creator (defaults to first superuser)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing categories before populating",
        )

    def handle(self, *args, **options):
        # Get the user to set as creator
        user_email = options.get("user_email")
        if user_email:
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with email "{user_email}" not found'))
                return
        else:
            user = User.objects.filter(is_admin=True).first()
            if not user:
                self.stdout.write(
                    self.style.ERROR("No superuser found. Please create one first or specify --user-email")
                )
                return

        # Clear existing categories if requested
        if options["clear"]:
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared all existing categories"))

        # Default wedding expense categories
        categories_data = [
            {"name": "Venue", "description": "Wedding venue rental, reception hall, outdoor spaces"},
            {"name": "Catering", "description": "Food, beverages, bar service, cake, desserts"},
            {"name": "Photography", "description": "Wedding photographer, videographer, photo booth"},
            {"name": "Flowers & Decorations", "description": "Bouquets, centerpieces, ceremony decorations, lighting"},
            {"name": "Wedding Attire", "description": "Wedding dress, suit, shoes, accessories, alterations"},
            {"name": "Beauty & Hair", "description": "Hair styling, makeup, manicure, pedicure, spa treatments"},
            {"name": "Stationery", "description": "Invitations, save the dates, programs, thank you cards"},
            {"name": "Rings & Jewelry", "description": "Engagement ring, wedding bands, jewelry for wedding party"},
            {"name": "Wedding Party", "description": "Gifts for bridesmaids, groomsmen, bachelor/bachelorette parties"},
            {"name": "Ceremony", "description": "Officiant fees, ceremony music, unity candles, programs"},
            {"name": "Rental Items", "description": "Chairs, tables, linens, tents, sound equipment"},
            {"name": "Guest Gifts", "description": "Favors, welcome bags, thank you gifts for guests"},
            {"name": "Weekend Food, Drinks & Supplies", "description": "Provisions for the rest of the weekend"},
            {"name": "Miscellaneous", "description": "Wedding insurance, tips, unexpected expenses, emergency fund"},
        ]

        created_count = 0
        updated_count = 0

        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data["name"],
                defaults={
                    "description": category_data["description"],
                    "created_by": user,
                    "updated_by": user,
                },
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            else:
                # Update description if category already exists
                if category.description != category_data["description"]:
                    category.description = category_data["description"]
                    category.updated_by = user
                    category.save()
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f"Updated category: {category.name}"))
                else:
                    self.stdout.write(self.style.NOTICE(f"Category already exists: {category.name}"))

        self.stdout.write(
            self.style.SUCCESS(f"\nSummary: {created_count} categories created, {updated_count} categories updated")
        )
        self.stdout.write(self.style.SUCCESS(f"Total categories in database: {Category.objects.count()}"))
