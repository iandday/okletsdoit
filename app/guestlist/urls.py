from django.urls import path

from . import views

app_name = "guestlist"

urlpatterns = [
    path("", views.guestlist_summary, name="guestlist_summary"),
    path("import/", views.guestlist_import, name="guestlist_import"),
    path("guests/", views.all_guests, name="all_guests"),
    path("guest_group_delete_modal", views.guest_group_delete_modal, name="guest_group_delete_modal"),
    path("guest_group/create/", views.guestgroup_create, name="guestgroup_create"),
    path("guest_group/<slug:group_slug>/", views.guestgroup_detail, name="guestgroup_detail"),
    path("guest_group/<slug:group_slug>/edit/", views.guestgroup_edit, name="guestgroup_edit"),
    path("guest_group/<slug:group_slug>/delete/", views.guest_group_delete, name="guest_group_delete"),
    path("guest_group/<slug:group_slug>/guest/create/", views.guest_create, name="guest_create_for_group"),
    path("guest/create/", views.guest_create, name="guest_create"),
    path("guest_data/", views.guest_data, name="guest_data"),
    path("guest_delete_modal", views.guest_delete_modal, name="guest_delete_modal"),
    path("guest/<slug:guest_slug>/", views.guest_detail, name="guest_detail"),
    path("guest/<slug:guest_slug>/edit/", views.guest_edit, name="guest_edit"),
    path("guest/<slug:guest_slug>/delete/", views.guest_delete, name="guest_delete"),
    path("export/address_labels/", views.address_csv_export, name="address_csv_export"),
]
