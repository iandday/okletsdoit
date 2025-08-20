from django import forms
from django.forms import ModelForm
from .models import Contact


class ContactForm(ModelForm):
    """Form for creating and editing contacts."""

    class Meta:
        model = Contact
        fields = ["name", "company", "email", "phone", "website", "category", "notes"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter contact name"}
            ),
            "company": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter company name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter email address"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter phone number"}
            ),
            "website": forms.URLInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "https://example.com"}
            ),
            "category": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "e.g., Vendor, Guest, Venue",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "",
                    "rows": 4,
                    "placeholder": "Enter any additional notes",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Contact Name"
        self.fields["company"].label = "Company"
        self.fields["email"].label = "Email Address"
        self.fields["phone"].label = "Phone Number"
        self.fields["website"].label = "Website URL"
        self.fields["category"].label = "Category"
        self.fields["notes"].label = "Notes"

        # Mark required fields
        self.fields["name"].required = False
        self.fields["company"].required = False
        self.fields["email"].required = False
        self.fields["phone"].required = False
        self.fields["website"].required = False
        self.fields["category"].required = False
        self.fields["notes"].required = False


class FileUploadForm(forms.Form):
    """Form for uploading files associated with a contact."""

    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "file-input file-input-bordered edit-card-field-value"}),
        help_text="Upload a file related to this contact",
    )
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter file name"}
        ),
        help_text="Enter a name for the uploaded file",
    )
    description = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter file description"}
        ),
        help_text="Enter a description for the uploaded file",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].label = "Upload File"


class ContactImportForm(forms.Form):
    """Form for importing contacts from Excel file."""

    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "file-input file-input-bordered file-input-primary w-full", "accept": ".xlsx,.xls"}
        ),
        help_text="Upload an Excel file with contact information",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["excel_file"].label = "Excel File"
