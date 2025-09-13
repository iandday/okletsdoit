from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
# from allauth.account.decorators import secure_admin_login

app_name = "okletsdoit"

# authentik login
# admin.autodiscover()
# admin.site.login = secure_admin_login(admin.site.login)

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("health/", include("health_check.urls")),
    path("expenses/", include("expenses.urls")),
    path("contacts/", include("contacts.urls")),
    path("lists/", include("list.urls")),
    path("deadline/", include("deadline.urls")),
    path("guestlist/", include("guestlist.urls")),
    path("attachments/", include("attachments.urls")),
    path("", include("core.urls")),
]

if "debug_toolbar" in settings.INSTALLED_APPS:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
