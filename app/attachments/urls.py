from django.urls import re_path as url
from . import views

app_name = "attachments"


urlpatterns = [
    url(
        r"^add-for/(?P<app_label>[\w\-]+)/(?P<model_name>[\w\-]+)/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$",
        views.add_attachment,
        name="add_attachment",
    ),
    url(r"^delete/(?P<slug>[\w\-]+)/$", views.delete_attachment, name="delete_attachment"),
]
