from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("venue/", views.venue, name="venue"),
    path("our-story/", views.our_story, name="our_story"),
    path("photos/", views.photos, name="photos"),
    path("rsvp/", views.rsvp, name="rsvp"),
]
