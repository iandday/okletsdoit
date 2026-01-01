from django import forms
from django.forms import ModelForm
from .models import Category, Expense


class CategoryForm(ModelForm):
    """Form for creating and editing categories."""

    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter category name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter category description",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Category Name"
        self.fields["description"].label = "Category Description"


class ExpenseForm(ModelForm):
    """Form for creating and editing expenses."""

    class Meta:
        model = Expense
        fields = [
            "item",
            "description",
            "date",
            "category",
            "vendor",
            "unit_price",
            "additional_price",
            "quantity",
            "estimated_amount",
            "actual_amount",
            "url",
        ]
        widgets = {
            "item": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter item name"}
            ),
            "description": forms.Textarea(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter description"}
            ),
            "date": forms.DateInput(attrs={"class": "input input-bordered edit-card-field-value", "type": "date"}),
            "category": forms.Select(attrs={"class": "select select-bordered edit-card-field-value"}),
            "vendor": forms.Select(attrs={"class": "select select-bordered edit-card-field-value"}),
            "quantity": forms.NumberInput(attrs={"class": "input input-bordered edit-card-field-value", "min": 1}),
            "unit_price": forms.NumberInput(
                attrs={"class": "input input-bordered edit-card-field-value", "step": 0.01}
            ),
            "additional_price": forms.NumberInput(
                attrs={"class": "input input-bordered edit-card-field-value", "step": 0.01}
            ),
            "estimated_amount": forms.NumberInput(
                attrs={"class": "input input-bordered edit-card-field-value", "step": 0.01}
            ),
            "actual_amount": forms.NumberInput(
                attrs={"class": "input input-bordered edit-card-field-value", "step": 0.01}
            ),
            "url": forms.URLInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter URL (optional)"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False
        self.fields["date"].required = False
        self.fields["category"].required = True
        self.fields["estimated_amount"].required = False
        self.fields["actual_amount"].required = False
        self.fields["quantity"].required = False
        self.fields["url"].required = False
