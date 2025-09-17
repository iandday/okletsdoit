from django.urls import path

from . import views

app_name = "contacts"

urlpatterns = [
    path("", views.contact_list, name="list"),
    path("create/", views.contact_create, name="create"),
    path("import/", views.contact_import, name="import"),
    path("template/", views.template_download, name="template_download"),
    path("contact_delete_modal/", views.contact_delete_modal, name="contact_delete_modal"),
    path("file_delete_modal/", views.file_delete_modal, name="file_delete_modal"),
    path("<slug:slug>/", views.contact_detail, name="detail"),
    path("<slug:slug>/edit/", views.contact_edit, name="contact_edit"),
    path("<slug:slug>/delete/", views.contact_delete, name="contact_delete"),
    path("<slug:slug>/upload/", views.file_upload, name="file_upload"),
    path("file/<slug:slug>/", views.file_detail, name="file_detail"),
    path("file/<slug:slug>/edit/", views.file_edit, name="file_edit"),
    path("file/<slug:slug>/delete/", views.file_delete, name="file_delete"),
]
