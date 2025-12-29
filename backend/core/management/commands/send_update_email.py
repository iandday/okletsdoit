from __future__ import annotations

import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum, F, DecimalField
from django.utils import timezone
from django.urls import reverse
from django.template.loader import render_to_string

from core.models import WeddingSettings
from deadline.models import Deadline
from expenses.models import Expense
from guestlist.models import Guest, GuestGroup

User = get_user_model()


class Command(BaseCommand):
    help = "Send a wedding planning update email to the bride and groom with deadlines, budget status, and other helpful information"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--recipients",
            nargs="+",
            help="Email addresses to send to (defaults to all superusers)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print the email content without sending",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        base_url = settings.EMAIL_URL_BASE

        # Get recipients
        if options.get("recipients"):
            recipients = options["recipients"]
        else:
            recipients = list(
                User.objects.filter(is_admin=True, email_notifications=True).values_list("email", flat=True)
            )

        if not recipients:
            self.stdout.write(
                self.style.ERROR(
                    "No recipients found. Please specify --recipients or users have enabled email notifications."
                )
            )
            return

        # Gather wedding data
        wedding_settings = WeddingSettings.objects.first()
        today = timezone.now().date()

        # Calculate days until wedding
        days_until_wedding = None
        if wedding_settings and wedding_settings.wedding_date:
            days_until_wedding = (wedding_settings.wedding_date - today).days

        # Get upcoming deadlines (next 30 days)
        upcoming_deadlines = Deadline.objects.filter(
            is_deleted=False,
            completed=False,
            due_date__isnull=False,
            due_date__gte=today,
            due_date__lte=today + datetime.timedelta(days=30),
        ).order_by("due_date")

        # Get overdue deadlines
        overdue_deadlines = Deadline.objects.filter(
            is_deleted=False, completed=False, due_date__isnull=False, due_date__lt=today
        ).order_by("due_date")

        # Get all deadlines stats
        total_deadlines = Deadline.objects.filter(is_deleted=False).count()
        completed_deadlines = Deadline.objects.filter(is_deleted=False, completed=True).count()
        pending_deadlines = total_deadlines - completed_deadlines
        completion_percentage = round((completed_deadlines / total_deadlines * 100), 1) if total_deadlines > 0 else 0

        # Budget information
        total_estimated = Expense.objects.filter(is_deleted=False).aggregate(
            total=Sum("estimated_amount", output_field=DecimalField(max_digits=40, decimal_places=2))
        )["total"] or Decimal("0.00")

        total_actual = Expense.objects.filter(is_deleted=False).aggregate(
            total=Sum("actual_amount", output_field=DecimalField(max_digits=40, decimal_places=2))
        )["total"] or Decimal("0.00")

        budget_variance = total_actual - total_estimated
        purchased_expenses = Expense.objects.filter(is_deleted=False, actual_amount__gt=0).count()
        total_expenses = Expense.objects.filter(is_deleted=False).count()

        # Guest list information
        total_guests = Guest.objects.filter(is_deleted=False).count()
        total_groups = GuestGroup.objects.filter(is_deleted=False).count()

        # Guests with RSVP responses
        guests_attending = Guest.objects.filter(is_deleted=False, responded=True, is_attending=True).count()

        guests_declined = Guest.objects.filter(is_deleted=False, responded=True, is_attending=False).count()

        guests_pending = Guest.objects.filter(is_deleted=False, responded=False).count()

        # Build email content
        if settings.DEBUG:
            subject = f"[DEV] Wedding Planning Update - {today.strftime('%B %d, %Y')}"
        else:
            subject = f"Wedding Planning Update - {today.strftime('%B %d, %Y')}"

        html_body = self._build_html_email_body(
            base_url=base_url,
            wedding_settings=wedding_settings,
            days_until_wedding=days_until_wedding,
            upcoming_deadlines=upcoming_deadlines,
            overdue_deadlines=overdue_deadlines,
            total_deadlines=total_deadlines,
            completed_deadlines=completed_deadlines,
            pending_deadlines=pending_deadlines,
            completion_percentage=completion_percentage,
            total_estimated=total_estimated,
            total_actual=total_actual,
            budget_variance=budget_variance,
            purchased_expenses=purchased_expenses,
            total_expenses=total_expenses,
            total_guests=total_guests,
            total_groups=total_groups,
            guests_attending=guests_attending,
            guests_declined=guests_declined,
            guests_pending=guests_pending,
        )

        # Plain text fallback
        plain_body = self._build_plain_email_body(
            wedding_settings=wedding_settings,
            days_until_wedding=days_until_wedding,
            upcoming_deadlines=upcoming_deadlines,
            overdue_deadlines=overdue_deadlines,
            total_deadlines=total_deadlines,
            completed_deadlines=completed_deadlines,
            pending_deadlines=pending_deadlines,
            completion_percentage=completion_percentage,
            total_estimated=total_estimated,
            total_actual=total_actual,
            budget_variance=budget_variance,
            purchased_expenses=purchased_expenses,
            total_expenses=total_expenses,
            total_guests=total_guests,
            total_groups=total_groups,
            guests_attending=guests_attending,
            guests_declined=guests_declined,
            guests_pending=guests_pending,
        )

        if dry_run:
            self.stdout.write(self.style.SUCCESS("=== DRY RUN MODE ==="))
            self.stdout.write(f"Subject: {subject}")
            self.stdout.write(f"Recipients: {', '.join(recipients)}")
            self.stdout.write(f"Base URL: {base_url}")
            self.stdout.write("\n=== HTML Content ===")
            self.stdout.write(html_body)
            self.stdout.write("\n=== Plain Text Fallback ===")
            self.stdout.write(plain_body)
            self.stdout.write(self.style.SUCCESS("\n=== END DRY RUN ==="))
        else:
            try:
                send_mail(
                    subject=subject,
                    message=plain_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipients,
                    fail_silently=False,
                    html_message=html_body,
                )
                self.stdout.write(self.style.SUCCESS(f"Update email sent successfully to {', '.join(recipients)}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to send email: {str(e)}"))

    def _build_html_email_body(self, base_url, **data):
        """Build the HTML email body using Django template"""
        # Prepare deadlines with URLs and calculated fields
        overdue_deadlines = []
        for deadline in data["overdue_deadlines"]:
            days_overdue = (timezone.now().date() - deadline.due_date).days
            deadline_url = f"{base_url}{reverse('deadline:deadline_detail', kwargs={'deadline_slug': deadline.slug})}"
            overdue_deadlines.append(
                {
                    "name": deadline.name,
                    "url": deadline_url,
                    "due_date": deadline.due_date,
                    "days_overdue": days_overdue,
                    "assigned_to": deadline.assigned_to,
                }
            )

        upcoming_deadlines = []
        for deadline in data["upcoming_deadlines"]:
            days_until = (deadline.due_date - timezone.now().date()).days
            deadline_url = f"{base_url}{reverse('deadline:deadline_detail', kwargs={'deadline_slug': deadline.slug})}"
            upcoming_deadlines.append(
                {
                    "name": deadline.name,
                    "url": deadline_url,
                    "due_date": deadline.due_date,
                    "days_until": days_until,
                    "assigned_to": deadline.assigned_to,
                }
            )

        # Calculate response rate
        response_rate = None
        if data["total_guests"] > 0 and (data["guests_attending"] > 0 or data["guests_declined"] > 0):
            response_rate = round(
                ((data["guests_attending"] + data["guests_declined"]) / data["total_guests"] * 100), 1
            )

        # Format currency values
        total_estimated_formatted = f"{data['total_estimated']:,.2f}"
        total_actual_formatted = f"{data['total_actual']:,.2f}"
        budget_variance_formatted = f"{data['budget_variance']:,.2f}"
        budget_variance_abs_formatted = f"{abs(data['budget_variance']):,.2f}"

        # Calculate days since wedding (for past weddings)
        days_since_wedding = (
            abs(data["days_until_wedding"]) if data["days_until_wedding"] and data["days_until_wedding"] < 0 else None
        )

        context = {
            "days_until_wedding": data["days_until_wedding"],
            "days_since_wedding": days_since_wedding,
            "total_deadlines": data["total_deadlines"],
            "completed_deadlines": data["completed_deadlines"],
            "completion_percentage": data["completion_percentage"],
            "pending_deadlines": data["pending_deadlines"],
            "overdue_deadlines": overdue_deadlines,
            "upcoming_deadlines": upcoming_deadlines,
            "total_estimated": data["total_estimated"],
            "total_actual": data["total_actual"],
            "budget_variance": data["budget_variance"],
            "total_estimated_formatted": total_estimated_formatted,
            "total_actual_formatted": total_actual_formatted,
            "budget_variance_formatted": budget_variance_formatted,
            "budget_variance_abs_formatted": budget_variance_abs_formatted,
            "purchased_expenses": data["purchased_expenses"],
            "total_expenses": data["total_expenses"],
            "total_guests": data["total_guests"],
            "total_groups": data["total_groups"],
            "guests_attending": data["guests_attending"],
            "guests_declined": data["guests_declined"],
            "guests_pending": data["guests_pending"],
            "response_rate": response_rate,
            "generated_date": timezone.now().strftime("%B %d, %Y at %I:%M %p"),
        }

        return render_to_string("email/wedding_update.html", context)

    def _build_plain_email_body(self, **data):
        """Build the plain text email body using Django template"""
        # Prepare deadlines with calculated fields
        overdue_deadlines = []
        for deadline in data["overdue_deadlines"]:
            days_overdue = (timezone.now().date() - deadline.due_date).days
            overdue_deadlines.append(
                {
                    "name": deadline.name,
                    "due_date": deadline.due_date,
                    "days_overdue": days_overdue,
                    "assigned_to": deadline.assigned_to,
                }
            )

        upcoming_deadlines = []
        for deadline in data["upcoming_deadlines"]:
            days_until = (deadline.due_date - timezone.now().date()).days
            upcoming_deadlines.append(
                {
                    "name": deadline.name,
                    "due_date": deadline.due_date,
                    "days_until": days_until,
                    "assigned_to": deadline.assigned_to,
                }
            )

        # Calculate response rate
        response_rate = None
        if data["total_guests"] > 0 and (data["guests_attending"] > 0 or data["guests_declined"] > 0):
            response_rate = round(
                ((data["guests_attending"] + data["guests_declined"]) / data["total_guests"] * 100), 1
            )

        # Format currency values
        total_estimated_formatted = f"{data['total_estimated']:,.2f}"
        total_actual_formatted = f"{data['total_actual']:,.2f}"
        budget_variance_formatted = f"{data['budget_variance']:,.2f}"
        budget_variance_abs_formatted = f"{abs(data['budget_variance']):,.2f}"

        # Calculate days since wedding (for past weddings)
        days_since_wedding = (
            abs(data["days_until_wedding"]) if data["days_until_wedding"] and data["days_until_wedding"] < 0 else None
        )

        context = {
            "days_until_wedding": data["days_until_wedding"],
            "days_since_wedding": days_since_wedding,
            "total_deadlines": data["total_deadlines"],
            "completed_deadlines": data["completed_deadlines"],
            "completion_percentage": data["completion_percentage"],
            "pending_deadlines": data["pending_deadlines"],
            "overdue_deadlines": overdue_deadlines,
            "upcoming_deadlines": upcoming_deadlines,
            "total_estimated": data["total_estimated"],
            "total_actual": data["total_actual"],
            "budget_variance": data["budget_variance"],
            "total_estimated_formatted": total_estimated_formatted,
            "total_actual_formatted": total_actual_formatted,
            "budget_variance_formatted": budget_variance_formatted,
            "budget_variance_abs_formatted": budget_variance_abs_formatted,
            "purchased_expenses": data["purchased_expenses"],
            "total_expenses": data["total_expenses"],
            "total_guests": data["total_guests"],
            "total_groups": data["total_groups"],
            "guests_attending": data["guests_attending"],
            "guests_declined": data["guests_declined"],
            "guests_pending": data["guests_pending"],
            "response_rate": response_rate,
            "generated_date": timezone.now().strftime("%B %d, %Y at %I:%M %p"),
        }

        return render_to_string("email/wedding_update.txt", context)
