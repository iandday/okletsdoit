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
        fields = [
            "item",
            "description",
            "is_completed",
            "quantity",
            "unit_price",
            "additional_price",
            "purchased",
            "associated_expense",
            "vendor",
            "url",
        ]
        widgets = {
            "item": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Enter item name"}),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Enter item description (optional)",
                    "rows": 2,
                }
            ),
            "quantity": forms.NumberInput(
                attrs={"class": "input input-bordered w-full", "placeholder": "Enter quantity", "min": 1}
            ),
            "purchased": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
            "unit_price": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter unit price",
                    "step": "0.01",
                    "min": 0,
                }
            ),
            "additional_price": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter additional price (optional)",
                    "step": "0.01",
                    "min": 0,
                }
            ),
            "is_completed": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
            "associated_expense": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "vendor": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "url": forms.URLInput(
                attrs={"class": "input input-bordered w-full", "placeholder": "Enter URL (optional)"}
            ),
        }


class ListImportForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "file-input file-input-bordered file-input-primary w-full", "accept": ".xlsx,.xls"}
        )
    )
