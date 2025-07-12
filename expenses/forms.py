from django import forms
from django.forms import ModelForm
from .models import Category


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
