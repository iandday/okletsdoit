"""
Utility functions for the core app.
"""

import io
import qrcode
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.db import models
from attachments.models import Attachment
from users.models import User


def generate_qr_code_attachment(
    url: str,
    name: str,
    model_instance: models.Model,
    uploaded_by: User,
    filename: str,
) -> Attachment:
    """
    Generate a QR code for the given URL and save it as an Attachment.

    Args:
        url: The URL to encode in the QR code
        name: Display name for the attachment
        model_instance: The model instance to attach the QR code to
        uploaded_by: The user creating the attachment
        filename: The filename for the QR code image (e.g., "qr_code_ABC123.png")

    Returns:
        The created Attachment instance
    """
    # delete any existing QR code attachment for this instance
    content_type = ContentType.objects.get_for_model(model_instance)
    Attachment.objects.filter(content_type=content_type, object_id=model_instance.pk).delete()

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save to BytesIO
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Create Attachment
    content_type = ContentType.objects.get_for_model(model_instance)
    attachment = Attachment(
        name=name,
        content_type=content_type,
        object_id=model_instance.pk,
        uploaded_by=uploaded_by,
    )
    attachment.attachment_file.save(
        filename,
        ContentFile(buffer.getvalue()),
        save=True,
    )

    return attachment
