# Tests for the attachments app
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from .models import Attachment
from .forms import AttachmentUploadForm


class DummyModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "attachments"


class AttachmentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="pw")
        self.obj = DummyModel.objects.create(name="dummy")
        self.file = SimpleUploadedFile("test.txt", b"hello world")

    def test_create_attachment(self):
        ct = ContentType.objects.get_for_model(self.obj)
        attachment = Attachment.objects.create(
            name="Test Attachment",
            attachment_file=self.file,
            content_type=ct,
            object_id=self.obj.pk,
            uploaded_by=self.user,
        )
        self.assertEqual(attachment.name, "Test Attachment")
        self.assertTrue(attachment.attachment_file)
        self.assertEqual(attachment.uploaded_by, self.user)
        self.assertFalse(attachment.is_deleted)

    def test_slug_autogeneration(self):
        ct = ContentType.objects.get_for_model(self.obj)
        attachment = Attachment.objects.create(
            name="Test Slug",
            attachment_file=self.file,
            content_type=ct,
            object_id=self.obj.pk,
            uploaded_by=self.user,
        )
        self.assertTrue(attachment.slug.startswith("test-slug"))

    def test_filename_property(self):
        ct = ContentType.objects.get_for_model(self.obj)
        attachment = Attachment.objects.create(
            name="FileNameTest",
            attachment_file=self.file,
            content_type=ct,
            object_id=self.obj.pk,
            uploaded_by=self.user,
        )
        self.assertEqual(attachment.filename, "test.txt")

    def test_manager_attachments_for_object(self):
        ct = ContentType.objects.get_for_model(self.obj)
        attachment = Attachment.objects.create(
            name="ManagerTest",
            attachment_file=self.file,
            content_type=ct,
            object_id=self.obj.pk,
            uploaded_by=self.user,
        )
        qs = Attachment.objects.attachments_for_object(self.obj)
        self.assertIn(attachment, qs)


class AttachmentFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="formuser", password="pw")
        self.obj = DummyModel.objects.create(name="dummyform")

    def test_upload_form_valid(self):
        file = SimpleUploadedFile("form.txt", b"form content")
        data = {"name": "FormTest", "description": "desc"}
        form = AttachmentUploadForm(data, {"attachment_file": file})
        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        ct = ContentType.objects.get_for_model(self.obj)
        instance.content_type = ct
        instance.object_id = self.obj.pk
        instance.uploaded_by = self.user
        instance.save()
        self.assertEqual(instance.name, "FormTest")


class AttachmentDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="deluser", password="pw")
        self.obj = DummyModel.objects.create(name="dummydelete")
        self.file = SimpleUploadedFile("del.txt", b"delete me")
        ct = ContentType.objects.get_for_model(self.obj)
        self.attachment = Attachment.objects.create(
            name="DeleteTest",
            attachment_file=self.file,
            content_type=ct,
            object_id=self.obj.pk,
            uploaded_by=self.user,
        )

    def test_delete_attachment(self):
        self.attachment.is_deleted = True
        self.attachment.save()
        self.assertTrue(self.attachment.is_deleted)
