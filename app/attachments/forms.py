from django.forms import ModelForm, ClearableFileInput, TextInput, Textarea, Select
from .models import Attachment


class AttachmentUploadForm(ModelForm):
    """Form for uploading files associated with a contact."""

    class Meta:
        model = Attachment
        fields = ["attachment_file", "name", "description"]
        widgets = {
            "attachment_file": ClearableFileInput(
                attrs={"class": "file-input file-input-bordered edit-card-field-value"}
            ),
            "name": TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter file name"}
            ),
            "description": Textarea(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter file description"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["attachment_file"].label = "Upload File"
