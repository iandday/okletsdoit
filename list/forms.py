from django import forms
from .models import List, ListEntry


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Enter list name"}),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Enter list description (optional)",
                    "rows": 3,
                }
            ),
        }


class ListEntryForm(forms.ModelForm):
    class Meta:
        model = ListEntry
        fields = ["item", "description", "is_completed"]
        widgets = {
            "item": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Enter item name"}),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Enter item description (optional)",
                    "rows": 2,
                }
            ),
            "is_completed": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
        }


class ListImportForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "file-input file-input-bordered file-input-primary w-full", "accept": ".xlsx,.xls"}
        )
    )
