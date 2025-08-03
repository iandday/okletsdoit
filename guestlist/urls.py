from django.urls import path

from . import views

app_name = "guestlist"

urlpatterns = [
    path("", views.guestlist_summary, name="guestlist_summary"),
    path("import/", views.guestlist_import, name="guestlist_import"),
    path("guests/", views.all_guests, name="all_guests"),
    path("group/create/", views.guestgroup_create, name="guestgroup_create"),
    path("group/<slug:group_slug>/", views.guestgroup_detail, name="guestgroup_detail"),
    path("group/<slug:group_slug>/edit/", views.guestgroup_edit, name="guestgroup_edit"),
    path("group/<slug:group_slug>/delete/", views.guestgroup_delete, name="guestgroup_delete"),
    path("group/<slug:group_slug>/guest/create/", views.guest_create, name="guest_create_for_group"),
    path("guest/create/", views.guest_create, name="guest_create"),
    path("guest/<slug:guest_slug>/", views.guest_detail, name="guest_detail"),
    path("guest/<slug:guest_slug>/edit/", views.guest_edit, name="guest_edit"),
    path("guest/<slug:guest_slug>/delete/", views.guest_delete, name="guest_delete"),
]
