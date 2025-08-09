from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("venue/", views.venue, name="venue"),
    path("our-story/", views.our_story, name="our_story"),
    path("photos/", views.photos, name="photos"),
    path("rsvp/", views.rsvp, name="rsvp"),
    path("timeline/", views.timeline_summary, name="timeline_summary"),
    path("timeline/import/", views.timeline_import, name="timeline_import"),
    path("timeline/create/", views.timeline_create, name="timeline_create"),
    path("timeline/<slug:timeline_slug>/", views.timeline_detail, name="timeline_detail"),
    path("timeline/<slug:timeline_slug>/edit/", views.timeline_edit, name="timeline_edit"),
    path("timeline/<slug:timeline_slug>/delete/", views.timeline_delete, name="timeline_delete"),
    path("idea/", views.idea_list, name="idea_list"),
    path("idea/template/download/", views.idea_template_download, name="idea_template_download"),
    path("idea/import/", views.idea_import, name="idea_import"),
    path("idea/<slug:idea_slug>/", views.idea_detail, name="idea_detail"),
    path("idea/<slug:idea_slug>/edit/", views.idea_edit, name="idea_edit"),
    path("idea/<slug:idea_slug>/delete/", views.idea_delete, name="idea_delete"),
    path("idea_create/", views.idea_create, name="idea_create"),
    path("csp-report/", views.csp_report, name="csp_report"),
]
