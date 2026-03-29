
from pathlib import Path

from django.test import TestCase
from django.test import override_settings

from core.models import WeddingSettings
from users.models import User


@override_settings(MEDIA_ROOT="/tmp/okletsdoit-test-media")
class WeddingSettingsTests(TestCase):
    def test_wedding_settings_generates_qr_attachment_on_first_save(self):
        admin_user = User.objects.create_user(email="admin@example.com", password="securepassword123")  # noqa: S106
        admin_user.is_admin = True
        admin_user.is_staff = True
        admin_user.save()

        wedding_settings = WeddingSettings.objects.create()
        wedding_settings.refresh_from_db()
        attachment = wedding_settings.rsvp_qr_code

        self.assertIsNotNone(wedding_settings.pk)
        self.assertIsNotNone(attachment)
        if attachment is None:
            self.fail("Expected WeddingSettings.save() to create a QR code attachment.")
        self.assertEqual(attachment.object_id, wedding_settings.pk)
        self.assertEqual(wedding_settings.rsvp_qr_code_url, attachment.attachment_file.url)
        self.assertTrue(Path(attachment.attachment_file.path).exists())
