from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("venue/", views.venue, name="venue"),
    path("our-story/", views.our_story, name="our_story"),
    path("photos/", views.photos, name="photos"),
    path("rsvp/", views.rsvp, name="rsvp"),
    path("task_list/", views.task_list, name="task_list"),
    path("task_list/<slug:task_list_slug>/", views.task_list_detail, name="task_list_detail"),
    path("task_list/<slug:task_list_slug>/create_task", views.task_create, name="task_create"),
    path("task_list/<slug:task_list_slug>/delete/", views.task_list_delete, name="task_list_delete"),
    path("task_list/<slug:task_list_slug>/edit/", views.task_list_edit, name="task_list_edit"),
    path("task_list_create/", views.task_list_create, name="task_list_create"),
    path("task_list/template/download/", views.download_template, name="template_download"),
    path("task/<slug:task_slug>/edit", views.task_edit, name="task_edit"),
    path("task/<slug:task_slug>/delete", views.task_delete, name="task_delete"),
    path("idea/", views.idea_list, name="idea_list"),
    path("idea/<slug:idea_slug>/", views.idea_detail, name="idea_detail"),
    path("idea/<slug:idea_slug>/edit/", views.idea_edit, name="idea_edit"),
    path("idea/<slug:idea_slug>/delete/", views.idea_delete, name="idea_delete"),
    path("idea_create/", views.idea_create, name="idea_create"),
    path("csp-report/", views.csp_report, name="csp_report"),
]
