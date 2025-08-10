from django import forms
from django.core.files.base import ContentFile
from .models import List, ListEntry
import importlib


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-form-color input-bordered w-full", "placeholder": "Enter list name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea input-form-color textarea-bordered w-full",
                    "placeholder": "Enter list description (optional)",
                    "rows": 3,
                }
            ),
        }


class ListEntryForm(forms.ModelForm):
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
            "order",
            "image",
        ]
        widgets = {
            "item": forms.TextInput(
                attrs={"class": "input input-bordered edit-card-field-value ", "placeholder": "Enter item name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered edit-card-field-value",
                    "placeholder": "Enter item description (optional)",
                    "rows": 2,
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter quantity",
                    "min": 1,
                }
            ),
            "purchased": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
            "unit_price": forms.NumberInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter unit price",
                    "step": "0.01",
                    "min": 0,
                }
            ),
            "additional_price": forms.NumberInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter additional price (optional)",
                    "step": "0.01",
                    "min": 0,
                }
            ),
            "is_completed": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
            "associated_expense": forms.Select(attrs={"class": "select select-bordered edit-card-field-value"}),
            "vendor": forms.Select(attrs={"class": "select select-bordered edit-card-field-value"}),
            "url": forms.URLInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter URL (optional)",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "file-input file-input-bordered edit-card-field-value",
                    "accept": ".jpg,.jpeg,.png,.webp,.gif,.heic,.heif,image/*",
                    "help_text": "Upload an image (HEIC supported; will be converted to JPEG).",
                }
            ),
            "order": forms.NumberInput(
                attrs={
                    "class": "input input-bordered edit-card-field-value",
                    "placeholder": "Enter order number (optional)",
                    "min": 0,
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


class ListImportForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "file-input file-input-bordered edit-card-field-value", "accept": ".xlsx,.xls"}
        )
    )
