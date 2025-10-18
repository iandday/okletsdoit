import importlib
from django import forms
from django.forms import ModelForm
from .models import Idea, Question, Timeline, Inspiration, WeddingSettings
from django.core.files.base import ContentFile


class IdeaForm(ModelForm):
    """Form for creating and editing ideas."""

    class Meta:
        model = Idea
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter idea name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
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


class TimelineImportForm(forms.Form):
    excel_file = forms.FileField(
        label="Excel File",
        help_text="Upload an Excel file (.xlsx) with timeline data",
        widget=forms.FileInput(attrs={"class": "file-input file-input-bordered w-full", "accept": ".xlsx"}),
    )


class TimelineForm(ModelForm):
    """Form for creating and editing timeline events."""

    class Meta:
        model = Timeline
        fields = ["name", "start", "end", "description", "confirmed", "published"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter event name"}
            ),
            "start": forms.DateTimeInput(
                attrs={"class": "input input-bordered edit-card-field-value", "type": "datetime-local"}
            ),
            "end": forms.DateTimeInput(
                attrs={"class": "input input-bordered edit-card-field-value", "type": "datetime-local"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "rows": 3,
                    "placeholder": "Enter event description",
                }
            ),
            "confirmed": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary edit-card-field-toggle"}),
            "published": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary edit-card-field-toggle"}),
        }


class InspirationForm(ModelForm):
    """Form for creating and editing inspirations."""

    # Override model ImageField with FileField to bypass default Pillow validation
    image = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "file-input file-input-bordered edit-card-field-value",
                "accept": ".jpg,.jpeg,.png,.webp,.gif,.heic,.heif,image/*",
                "help_text": "Upload an image (HEIC supported; will be converted to JPEG).",
            }
        ),
        label="Image",
    )

    class Meta:
        model = Inspiration
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value", "placeholder": "Enter inspiration name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "rows": 3,
                    "placeholder": "Enter inspiration description (optional)",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "file-input file-input-bordered edit-card-field-value",
                    "accept": ".jpg,.jpeg,.png,.webp,.gif,.heic,.heif,image/*",
                    "help_text": "Upload an image (HEIC supported; will be converted to JPEG).",
                }
            ),
        }

    def clean_image(self):
        image_file = self.cleaned_data.get("image")
        if not image_file:
            return image_file

        content_type = getattr(image_file, "content_type", "") or ""
        name_lower = (getattr(image_file, "name", "") or "").lower()
        is_heic = content_type in ("image/heic", "image/heif") or name_lower.endswith((".heic", ".heif"))
        if not is_heic:
            return image_file

        raw_bytes = None
        try:
            from io import BytesIO
            from PIL import Image

            try:
                pillow_heif = importlib.import_module("pillow_heif")
                if hasattr(pillow_heif, "register_heif_opener"):
                    pillow_heif.register_heif_opener()
            except Exception:
                pass

            raw_bytes = image_file.read()
            pil_img = Image.open(BytesIO(raw_bytes))
            if pil_img.mode in ("P", "LA"):
                pil_img = pil_img.convert("RGBA")
            if pil_img.mode in ("RGBA", "LA"):
                from PIL import Image as PILImage

                bg = PILImage.new("RGB", pil_img.size, (255, 255, 255))
                bg.paste(pil_img, mask=pil_img.split()[-1])
                pil_img = bg
            elif pil_img.mode != "RGB":
                pil_img = pil_img.convert("RGB")

            out = BytesIO()
            pil_img.save(out, format="JPEG", quality=85, optimize=True)
            out.seek(0)

            new_name = (name_lower.rsplit(".", 1)[0] if "." in name_lower else name_lower) + ".jpg"
            return ContentFile(out.read(), name=new_name)
        except Exception:
            # Reset pointer or return original bytes if read already
            try:
                if raw_bytes is not None:
                    return ContentFile(raw_bytes, name=getattr(image_file, "name", "upload.heic"))
                image_file.seek(0)
            except Exception:
                pass
            return image_file


class QuestionForm(forms.ModelForm):
    """
    Form for creating and editing questions.
    """

    class Meta:
        model = Question
        fields = ["question", "answer", "order", "published"]
        widgets = {
            "question": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter question text",
                    "required": True,
                },
            ),
            "answer": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "rows": 40,
                    "placeholder": "Enter answer text",
                    "required": True,
                }
            ),
            "order": forms.NumberInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter order",
                    "required": True,
                },
            ),
            "published": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary edit-card-field-toggle",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question"].label = "Question"
        self.fields["answer"].label = "Answer"
        self.fields["answer"].required = False


class WeddingSettingsForm(ModelForm):
    """Form for editing wedding settings."""

    class Meta:
        model = WeddingSettings
        fields = [
            "allow_rsvp",
            "wedding_date",
        ]
        widgets = {
            "allow_rsvp": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary edit-card-field-toggle"}),
            "wedding_date": forms.DateInput(
                attrs={"class": "input input-bordered edit-card-field-value", "type": "date"}
            ),
        }
