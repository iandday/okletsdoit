from django.urls import path

from . import views

app_name = "list"

urlpatterns = [
    path("", views.list_summary, name="summary"),
    path("create/", views.list_create, name="create"),
    path("import/", views.list_import, name="import"),
    path("template_download/", views.template_download, name="template_download"),
    path("<slug:list_slug>/", views.list_detail, name="detail"),
    path("<slug:list_slug>/edit/", views.list_edit, name="edit"),
    path("<slug:list_slug>/delete/", views.list_delete, name="delete"),
    path("<slug:list_slug>/entries/create/", views.list_entry_create, name="entry_create"),
    path("entries/<slug:entry_slug>/", views.list_entry_detail, name="entry_detail"),
    path("entries/<slug:entry_slug>/edit/", views.list_entry_edit, name="entry_edit"),
    path("entries/<slug:entry_slug>/delete/", views.list_entry_delete, name="entry_delete"),
]
