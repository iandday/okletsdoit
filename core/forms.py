from django import forms
from django.forms import ModelForm
from .models import Idea
from users.models import User



class IdeaForm(ModelForm):
    """Form for creating and editing ideas."""

    class Meta:
        model = Idea
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Enter idea name"}),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full h-100",
                    "rows": 40,
                    "placeholder": "Enter idea description",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Idea Name"
        self.fields["description"].label = "Description"
        self.fields["description"].required = False


class IdeaImportForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "file-input file-input-bordered file-input-primary w-full", "accept": ".xlsx,.xls"}
        )
    )
