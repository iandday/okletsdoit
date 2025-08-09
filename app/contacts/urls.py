from django.urls import path

from . import views

app_name = "contacts"

urlpatterns = [
    path("", views.contact_list, name="list"),
    path("create/", views.contact_create, name="create"),
    path("import/", views.contact_import, name="import"),
    path("template/", views.template_download, name="template_download"),
    path("<slug:slug>/", views.contact_detail, name="detail"),
    path("<slug:slug>/edit/", views.contact_update, name="update"),
    path("<slug:slug>/delete/", views.contact_delete, name="delete"),
]
