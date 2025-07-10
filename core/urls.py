from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("venue/", views.venue, name="venue"),
    path("our-story/", views.our_story, name="our_story"),
    path("photos/", views.photos, name="photos"),
    path("rsvp/", views.rsvp, name="rsvp"),
    path("task_list/", views.task_list, name="task_list"),
    path("task_list/<slug:task_list_slug>/", views.task_list_detail, name="task_list_detail"),
    path("task_list/<slug:task_list_slug>/delete/", views.task_list_delete, name="task_list_delete"),
    path("task_list/<slug:task_list_slug>/edit/", views.task_list_edit, name="task_list_edit"),
    path("task_list_create/", views.task_list_create, name="task_list_create"),
    path("task_list/template/download/", views.download_template, name="template_download"),
    path("task/<slug:task_slug>/edit", views.task_edit, name="task_edit"),
    path("task/<slug:task_slug>/delete", views.task_delete, name="task_delete"),
]
