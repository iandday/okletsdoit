import datetime
import uuid

from django.db import models
from django.db.models import Sum, F, DecimalField
from django.utils.text import slugify
from decimal import Decimal
from users.models import User


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_by_category", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_category", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_category")]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    estimated_amount = models.DecimalField(max_digits=40, decimal_places=2, blank=True, null=True)
    actual_amount = models.DecimalField(max_digits=40, decimal_places=2, blank=True, null=True)
    url = models.URLField(
        blank=True,
        null=True,
        max_length=1000,
        help_text="URL for this item, e.g., a link to an online store or product page",
    )
    created_by = models.ForeignKey(User, related_name="created_by_expense", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, related_name="updated_by_expense", on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def completed(self):
        if self.actual_amount is not None and self.actual_amount > 0:
            return True
        return False

    @property
    def calculated_price(self):
        # calculate the sum of the total_price values for all associated ListEntry objects
        return self.list_entries.filter(is_deleted=False).aggregate(
            total_price=Sum(
                F("total_price"),
                output_field=DecimalField(max_digits=100, decimal_places=2),
            )
        )["total_price"] or Decimal("0.00")

    def calculated_estimated_amount(self) -> Decimal:
        """Calculate the sum of total_price fields for all associated list_entries that are not marked purchased"""
        return self.list_entries.filter(is_deleted=False).aggregate(
            total_price=Sum(
                F("total_price"),
                output_field=DecimalField(max_digits=100, decimal_places=2),
            )
        )["total_price"] or Decimal("0.00")

    def calculated_actual_amount(self) -> Decimal:
        """Calculate the sum of total_price fields for all associated list_entries that are marked purchased"""
        return self.list_entries.filter(purchased=True, is_deleted=False).aggregate(
            total_price=Sum(
                F("total_price"),
                output_field=DecimalField(max_digits=100, decimal_places=2),
            )
        )["total_price"] or Decimal("0.00")

    def __str__(self):
        return self.item

    class Meta:
        ordering = ["-date", "item"]
        verbose_name_plural = "Expenses"
        constraints = [models.UniqueConstraint(fields=["item", "category"], name="unique_expense_item_category")]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.item)
            slug = base_slug
            counter = 1

            while Expense.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        # update estimated_amount and actual_amount for expenses with associated list entries
        if self.list_entries.exists():
            self.estimated_amount = self.calculated_estimated_amount()
            self.actual_amount = self.calculated_actual_amount()
        super().save(*args, **kwargs)
