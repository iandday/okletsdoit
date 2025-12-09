import logging
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext
from .forms import AttachmentUploadForm
from .models import Attachment
# Create your views here.

logger = logging.getLogger(__name__)


@login_required
def add_attachment(
    request: HttpRequest,
    app_label: str,
    model_name: str,
    pk: str,
):
    next_ = request.GET.get("next", "/")

    if request.method != "POST":
        messages.error(request, "Invalid request method.")

    model_class = apps.get_model(app_label, model_name)
    obj = get_object_or_404(model_class, pk=pk)
    form = AttachmentUploadForm(request.POST, request.FILES)

    if form.is_valid():
        attachment: Attachment = form.save(commit=False)
        attachment.content_object = obj
        attachment.uploaded_by = request.user
        attachment.save()
        messages.success(request, f"Attached {attachment.filename}")
    else:
        messages.error(request, "Failed to attach file.")
    return HttpResponseRedirect(next_)


@login_required
def delete_attachment(request, attachment_pk):
    g = get_object_or_404(Attachment, pk=attachment_pk)
    if (request.user.has_perm("attachments.delete_attachment") and request.user == g.creator) or request.user.has_perm(
        "attachments.delete_foreign_attachments"
    ):
        g.is_deleted = True
        g.save()
        messages.success(request, gettext("Your attachment was deleted."))
    next_ = request.GET.get("next") or "/"
    return HttpResponseRedirect(next_)
