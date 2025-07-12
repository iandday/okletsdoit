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
                attrs={"class": "input input-bordered w-full", "placeholder": "Enter category name"}
            ),
            "description": forms.Textarea(
                attrs={"class": "input input-bordered w-full", "placeholder": "Enter category description"}
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
        fields = ["item", "description", "date", "category", "quantity", "estimated_amount", "actual_amount"]
        widgets = {
            "item": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Enter item name"}),
            "description": forms.Textarea(
                attrs={"class": "input input-bordered w-full", "placeholder": "Enter description"}
            ),
            "date": forms.DateInput(attrs={"class": "input input-bordered w-full", "type": "date"}),
            "category": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "quantity": forms.NumberInput(attrs={"class": "input input-bordered w-full", "min": 1}),
            "estimated_amount": forms.NumberInput(attrs={"class": "input input-bordered w-full", "step": 0.01}),
            "actual_amount": forms.NumberInput(attrs={"class": "input input-bordered w-full", "step": 0.01}),
        }
