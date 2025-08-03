from django import forms
from .models import GuestGroup, Guest


class GuestlistImportForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "file-input file-input-bordered input-form-color file-input-primary w-full",
                "accept": ".xlsx,.xls",
            }
        )
    )


class GuestGroupForm(forms.ModelForm):
    class Meta:
        model = GuestGroup
        fields = ["name", "notes", "email", "phone", "address", "city", "state", "zip_code", "relationship", "priority"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter group name"}
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Enter notes (optional)",
                    "rows": 3,
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter email"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter phone number"}
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter address",
                }
            ),
            "city": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter city"}
            ),
            "state": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter state"}
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter zip code"}
            ),
            "relationship": forms.Select(attrs={"class": "select select-bordered edit-card-field-value"}),
            "priority": forms.Select(attrs={"class": "select select-bordered edit-card-field-value"}),
        }


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            "first_name",
            "last_name",
            "group",
            "plus_one",
            "is_invited",
            "is_attending",
            "responded",
            "overnight",
            "notes",
            "response_notes",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter last name"}
            ),
            "group": forms.Select(attrs={"class": "select select-bordered edit-card-field-value"}),
            "plus_one": forms.CheckboxInput(attrs={"class": "edit-card-field-toggle"}),
            "is_invited": forms.CheckboxInput(attrs={"class": "edit-card-field-toggle"}),
            "is_attending": forms.CheckboxInput(attrs={"class": "edit-card-field-toggle"}),
            "responded": forms.CheckboxInput(attrs={"class": "edit-card-field-toggle"}),
            "overnight": forms.CheckboxInput(attrs={"class": "edit-card-field-toggle"}),
            "notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Enter notes (optional)",
                    "rows": 3,
                }
            ),
            "response_notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Enter response notes (optional)",
                    "rows": 2,
                }
            ),
        }
