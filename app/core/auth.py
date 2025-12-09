"""
Custom authentication classes for Django Ninja API
"""

from ninja.security import APIKeyHeader
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from allauth.headless.adapter import get_adapter
from allauth.headless.contrib.ninja.security import x_session_token_auth


class ServiceTokenAuth(APIKeyHeader):
    """
    Backend-to-backend service token authentication.
    Used for SSR requests from the SvelteKit frontend.
    """

    param_name = "X-Service-Token"

    def authenticate(self, request, key):
        """Authenticate using service token"""
        service_token = getattr(settings, "SERVICE_TOKEN", None)
        if service_token and key == service_token:
            return AnonymousUser()
        return None


class MultiAuth:
    """
    Combines multiple authentication methods.
    Tries each auth method in order until one succeeds.
    """

    def __init__(self, *auth_methods):
        self.auth_methods = auth_methods

    def __call__(self, request):
        for auth in self.auth_methods:
            if callable(auth):
                user = auth(request)
            else:
                # For Django Ninja security classes
                auth_result = auth.authenticate(request, request.headers.get(auth.param_name))
                user = auth_result

            if user:
                request.auth = user
                return user
        return None


# Create reusable auth instances
service_token_auth = ServiceTokenAuth()
multi_auth = MultiAuth(service_token_auth, x_session_token_auth)
