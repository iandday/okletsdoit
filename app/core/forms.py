import importlib
from typing import Any

from django import forms
from django.forms import BaseInlineFormSet, BaseModelFormSet, ModelForm, modelformset_factory, inlineformset_factory

from .models import (
    Idea,
    Question,
    Timeline,
    Inspiration,
    WeddingSettings,
    RsvpQuestion,
    RsvpQuestionChoice,
)
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
                    # "required": True,
                },
            ),
            "answer": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "rows": 40,
                    "placeholder": "Enter answer text",
                    # "required": True,
                }
            ),
            "order": forms.NumberInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter order",
                    # "required": True,
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
            "wedding_date",
            "allow_rsvp",
            "rsvp_accept_button",
            "rsvp_decline_button",
            "rsvp_attending_label",
            "rsvp_accommodation_label",
            "rsvp_vip_label",
            "rsvp_accept_intro",
            "rsvp_accommodation_intro",
            "rsvp_vip_intro",
            "rsvp_success_headline",
            "rsvp_accept_success_message",
            "rsvp_decline_success_message",
            "standard_group_label",
            "vip_group_label",
            "rsvp_show_accommodation_intro",
            "rsvp_show_vip_intro",
            "rsvp_enable_email_updates",
            "rsvp_email_update_label",
        ]
        labels = {
            "wedding_date": "Wedding Date",
            "allow_rsvp": "Allow RSVP",
            "rsvp_accept_button": "RSVP Accept Button Text",
            "rsvp_decline_button": "RSVP Decline Button Text",
            "rsvp_attending_label": "RSVP Attending Checkbox Label",
            "rsvp_accommodation_label": "RSVP Accommodation Checkbox Label",
            "rsvp_vip_label": "RSVP VIP Checkbox Label",
            "rsvp_accept_intro": "RSVP Accept Page Intro Section",
            "rsvp_accommodation_intro": "RSVP Accept Page Accommodation Intro Section",
            "rsvp_vip_intro": "RSVP Accept Page VIP Intro Section",
            "rsvp_success_headline": "RSVP Success Headline",
            "rsvp_accept_success_message": "RSVP Accept Success Message",
            "rsvp_decline_success_message": "RSVP Decline Success Message",
            "standard_group_label": "Standard Group Label",
            "vip_group_label": "VIP Group Label",
            "rsvp_show_accommodation_intro": "Show Accommodation Intro on RSVP Form",
            "rsvp_show_vip_intro": "Show VIP Intro on RSVP Form",
            "rsvp_enable_email_updates": "Enable Email Updates Option in RSVP",
            "rsvp_email_update_label": "Email Updates Opt-in Label",
        }
        widgets = {
            "allow_rsvp": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary edit-card-field-toggle"}),
            "wedding_date": forms.DateInput(
                attrs={"class": "input input-bordered edit-card-field-value", "type": "date"}
            ),
            "rsvp_accept_button": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter RSVP Accept Button Text",
                }
            ),
            "rsvp_decline_button": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter RSVP Decline Button Text",
                }
            ),
            "rsvp_attending_label": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter RSVP Attending Label Text",
                }
            ),
            "rsvp_accommodation_label": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter RSVP Overnight Label Text",
                }
            ),
            "rsvp_vip_label": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter RSVP VIP Label Text",
                }
            ),
            "rsvp_accept_intro": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "rows": 10,
                    "placeholder": "Enter RSVP Accept Intro Text",
                }
            ),
            "rsvp_accommodation_intro": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "rows": 10,
                    "placeholder": "Enter RSVP Accommodation Intro Text",
                }
            ),
            "rsvp_vip_intro": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "rows": 10,
                    "placeholder": "Enter RSVP VIP Intro Text",
                }
            ),
            "rsvp_success_headline": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter RSVP Success Headline",
                }
            ),
            "rsvp_accept_success_message": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "rows": 3,
                    "placeholder": "Enter RSVP Accept Success Message",
                }
            ),
            "rsvp_decline_success_message": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "rows": 3,
                    "placeholder": "Enter RSVP Decline Success Message",
                }
            ),
            "standard_group_label": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter Standard Group Label",
                }
            ),
            "vip_group_label": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter VIP Group Label",
                }
            ),
            "rsvp_show_accommodation_intro": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary edit-card-field-toggle",
                }
            ),
            "rsvp_show_vip_intro": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary edit-card-field-toggle",
                }
            ),
            "rsvp_enable_email_updates": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary edit-card-field-toggle",
                }
            ),
            "rsvp_email_update_label": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter Email Updates Opt-in Label",
                }
            ),
        }


class RsvpQuestionForm(ModelForm):
    class Meta:
        model = RsvpQuestion
        fields = ["text", "question_type", "order", "published"]  # , "created_by"]
        widgets = {
            "text": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter the question text shown to guests",
                }
            ),
            "question_type": forms.Select(
                attrs={"class": "select select-bordered edit-card-field-value w-48"},
            ),
            "order": forms.NumberInput(attrs={"class": "input input-bordered edit-card-field-value w-24"}),
            "published": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary edit-card-field-toggle"}),
            # "created_by": forms.HiddenInput(),
        }
        labels = {
            "text": "Question",
            "question_type": "Question Type",
            "order": "Order",
            "published": "Published",
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # Make the text field larger in admin-like UIs
        self.fields["text"].widget.attrs.setdefault("rows", 2)


class RsvpQuestionChoiceForm(ModelForm):
    class Meta:
        model = RsvpQuestionChoice
        fields = ["choice_text", "order"]
        labels = {"choice_text": "Choice"}
        widgets = {
            "choice_text": forms.TextInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Choice (e.g. Yes)",
                }
            ),
            "order": forms.NumberInput(attrs={"class": "input input-bordered edit-card-field-value w-24"}),
        }
        labels = {"choice_text": "Choice"}


class RsvpQuestionChoiceChildFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = RsvpQuestionChoice.objects.filter(question=self.instance, is_deleted=False)
