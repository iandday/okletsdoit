from django import forms
from .models import GuestGroup, Guest, RsvpSubmission


class GuestlistImportForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "file-input file-input-bordered input-form-color file-input-primary w-full",
                "accept": ".xlsx,.xls",
            }
        )
    )


class RsvpCodeForm(forms.Form):
    rsvp_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered edit-card-field-value",
                "placeholder": "Enter your RSVP code",
            }
        ),
        label="Please provide your RSVP code to respond",
    )


class GuestGroupForm(forms.ModelForm):
    class Meta:
        model = GuestGroup
        fields = [
            "name",
            "notes",
            "email",
            "phone",
            "address_name",
            "address",
            "address_two",
            "city",
            "state",
            "zip_code",
            "relationship",
            "associated_with",
            "priority",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter group name"}
            ),
            "address_name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter address name"}
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
            "address_two": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter address line 2",
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
            "associated_with": forms.Select(attrs={"class": "select select-bordered edit-card-field-value"}),
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
            "accept_accommodation",
            "accept_vip",
            "accommodation",
            "notes",
        ]

        labels = {
            "is_invited": "Invited",
            "is_attending": "Attending",
        }

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
            "accommodation": forms.CheckboxInput(attrs={"class": "edit-card-field-toggle"}),
            "accept_accommodation": forms.CheckboxInput(attrs={"class": "edit-card-field-toggle"}),
            "accept_vip": forms.CheckboxInput(attrs={"class": "edit-card-field-toggle"}),
            "notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Enter notes (optional)",
                    "rows": 3,
                }
            ),
        }


class GuestRSVPForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            "first_name",
            "last_name",
            "is_attending",
            "accept_accommodation",
            "accept_vip",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter last name"}
            ),
            "is_attending": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
            "accept_accommodation": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
            "accept_vip": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
        }


class RsvpSubmissionForm(forms.ModelForm):
    class Meta:
        model = RsvpSubmission
        fields = [
            "notes",
        ]

        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Enter any additional notes (optional)",
                    "rows": 3,
                }
            ),
        }
