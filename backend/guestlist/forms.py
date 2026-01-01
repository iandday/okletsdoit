from core.models import RsvpQuestion, RsvpQuestionChoice
from django import forms

from .models import Guest
from .models import GuestGroup
from .models import RsvpQuestionResponse
from .models import RsvpSubmission


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
            "email_updates",
            "email_address",
        ]

        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Enter any additional notes (optional)",
                    "rows": 3,
                }
            ),
            "email_updates": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
            "email_address": forms.EmailInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter your email address"}
            ),
        }


class RsvpQuestionResponseForm(forms.ModelForm):
    question_type = forms.CharField(widget=forms.HiddenInput())
    response_choices = forms.ModelMultipleChoiceField(
        queryset=RsvpQuestionChoice.objects.filter(is_deleted=False),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "space-y-2 checkbox-group"}),
        required=False,
    )

    class Meta:
        model = RsvpQuestionResponse
        fields = [
            "submission",
            "question",
            "response_text",
            "response_choices",
        ]

        widgets = {
            "submission": forms.HiddenInput(),
            "response_text": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Enter your response",
                    "rows": 3,
                }
            ),
            "question": forms.HiddenInput(),
        }

    # populate dynamic labels and initial values
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        q_id = self.initial.get("question") or self.data.get(self.add_prefix("question"))
        if q_id:
            q_obj = RsvpQuestion.objects.filter(pk=q_id).first()
            if q_obj:
                self.fields["response_choices"].queryset = RsvpQuestionChoice.objects.filter(question=q_obj)  # pyright: ignore[reportAttributeAccessIssue]
                self.fields["response_text"].label = q_obj.text
                self.fields["response_choices"].label = q_obj.text
                self.fields["question_type"].initial = q_obj.question_type
