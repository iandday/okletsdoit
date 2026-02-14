from django.apps import AppConfig


class GuestlistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "guestlist"

    def ready(self):
        # Import tasks to ensure they're registered with Celery
        import guestlist.tasks  # noqa: F401
