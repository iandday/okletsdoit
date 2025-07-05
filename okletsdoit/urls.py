from django.contrib import admin
from django.urls import include, path

from core import views as core
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core.home, name="home"),
    path("venue/", core.venue, name="venue"),
    path("our-story/", core.our_story, name="our_story"),
    path("health/", include("health_check.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
