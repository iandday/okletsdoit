"""
Utility functions for the core app.
"""

import io
import math
import segno
from PIL import Image, ImageDraw
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.db import models
from attachments.models import Attachment
from users.models import User


def create_heart_logo(size: int) -> Image.Image:
    """
    Create a red heart logo image.

    Args:
        size: The size of the heart logo (width and height in pixels)

    Returns:
        PIL Image with red heart
    """
    # Create transparent image
    heart = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(heart)

    # Calculate heart shape coordinates
    center_x = size // 2
    center_y = size // 2
    scale = size / 80  # Scale factor for the heart shape

    # Draw heart shape using a polygon
    points = []
    for angle in range(0, 360, 2):
        t = math.radians(angle)
        # Parametric equations for a heart shape
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))

        # Scale and center the heart
        x = center_x + (x * scale)
        y = center_y + (y * scale) - size * 0.05  # Slight upward offset
        points.append((x, y))

    # Draw filled heart in red (#ef4444)
    draw.polygon(points, fill=(239, 68, 68, 255))

    return heart


def generate_qr_code_attachment(
    url: str,
    name: str,
    model_instance: models.Model,
    uploaded_by: User,
    filename: str,
    heart_logo: bool = False,
) -> Attachment:
    """
    Generate a QR code for the given URL and save it as an Attachment.

    Args:
        url: The URL to encode in the QR code
        name: Display name for the attachment
        model_instance: The model instance to attach the QR code to
        uploaded_by: The user creating the attachment
        filename: The filename for the QR code image (e.g., "qr_code_ABC123.png")
        heart_logo: If True, adds a red heart logo to the center (default: False)

    Returns:
        The created Attachment instance
    """
    # delete any existing QR code attachment for this instance
    content_type = ContentType.objects.get_for_model(model_instance)
    Attachment.objects.filter(content_type=content_type, object_id=model_instance.pk).delete()

    # Generate QR code with high error correction for logo
    error_level = "H" if heart_logo else "L"
    qr = segno.make(url, error=error_level, boost_error=False)

    # Save to BytesIO as PNG first
    buffer = io.BytesIO()

    if heart_logo:
        # Generate base QR code image
        qr.save(buffer, kind="png", scale=10, border=1, dark="black", light="white")
        buffer.seek(0)
        img = Image.open(buffer).convert("RGBA")

        # Create heart logo (50% of QR code - maximum safe size with high error correction)
        logo_size = int(img.size[0] * 0.5)
        heart = create_heart_logo(logo_size)
        logo_pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        img.paste(heart, logo_pos, heart)

        # Save final image
        buffer = io.BytesIO()
        img.convert("RGB").save(buffer, format="PNG")
        buffer.seek(0)
    else:
        qr.save(buffer, kind="png", scale=10, border=1, dark="black", light="white")
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
