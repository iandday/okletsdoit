from django.urls import path

from . import views

app_name = "deadline"

urlpatterns = [
    path("", views.deadline_summary, name="deadline_summary"),
    path("create/", views.deadline_create, name="deadline_create"),
    path("import/", views.deadline_import, name="deadline_import"),
    path("<slug:deadline_slug>/edit", views.deadline_edit, name="deadline_edit"),
    path("<slug:deadline_slug>/delete", views.deadline_delete, name="deadline_delete"),
    path("list/create/", views.deadline_list_create, name="deadline_list_create"),
    path("list/<slug:deadline_list_slug>/", views.deadline_list_detail, name="deadline_list_detail"),
    path("list/<slug:deadline_list_slug>/delete/", views.deadline_list_delete, name="deadline_list_delete"),
    path("list/<slug:deadline_list_slug>/edit/", views.deadline_list_edit, name="deadline_list_edit"),
]
