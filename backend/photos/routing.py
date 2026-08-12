from django.urls import path

from .consumers import PhotoUpdatesConsumer

websocket_urlpatterns = [
    path("ws/photos/", PhotoUpdatesConsumer.as_asgi()),
]
