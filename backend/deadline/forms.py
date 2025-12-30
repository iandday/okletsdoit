from django import forms
from django.utils import timezone

from .models import Deadline, DeadlineList
from users.models import User


class DeadlineImportForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "file-input file-input-bordered input-form-color file-input-primary w-full",
                "accept": ".xlsx,.xls",
            }
        )
    )


class DeadlineListForm(forms.ModelForm):
    class Meta:
        model = DeadlineList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input edit-card-field-value", "placeholder": "Enter list name"}),
        }
        labels = {
            "name": "List Name",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadline
        fields = ["name", "description", "deadline_list", "due_date", "assigned_to", "completed", "completed_note"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input edit-card-field-value", "placeholder": "Enter deadline name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Enter description (optional)",
                    "rows": 3,
                }
            ),
            "deadline_list": forms.Select(attrs={"class": "select select-bordered edit-card-field-value"}),
            "due_date": forms.DateInput(attrs={"class": "input input-bordered edit-card-field-value", "type": "date"}),
            "assigned_to": forms.Select(attrs={"class": "select select-bordered w-full edit-card-field-value"}),
            "completed": forms.CheckboxInput(attrs={"class": "edit-card-field-toggle"}),
            "completed_note": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Add completion notes (optional)",
                    "rows": 2,
                }
            ),
        }
        labels = {
            "name": "Deadline Name",
            "description": "Description",
            "deadline_list": "Deadline List",
            "due_date": "Due Date",
            "assigned_to": "Assigned To",
            "completed": "Mark as Completed",
            "completed_note": "Completion Notes",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter deadline lists to only show those created by the user
        if user:
            self.fields["deadline_list"].queryset = DeadlineList.objects.filter(created_by=user, is_deleted=False)

            # Filter assigned_to to active users
            self.fields["assigned_to"].queryset = User.objects.filter(is_active=True)
            self.fields["assigned_to"].empty_label = "Unassigned"

        # Set required fields
        self.fields["name"].required = True
        self.fields["deadline_list"].required = True

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date and due_date < timezone.now().date():
            # Allow past dates but show a warning in the template
            pass
        return due_date

    def clean(self):
        cleaned_data = super().clean()
        completed = cleaned_data.get("completed")

        # If marking as completed, set completed_at timestamp
        if completed and not self.instance.completed_at:
            self.instance.completed_at = timezone.now()
        elif not completed:
            # If unchecking completed, clear completed_at and completed_note
            self.instance.completed_at = None
            cleaned_data["completed_note"]
