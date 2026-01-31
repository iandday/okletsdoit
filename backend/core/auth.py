"""
Custom authentication classes for Django Ninja API
"""

from ninja.security import APIKeyHeader, SessionAuth
from django.conf import settings
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
            # Return the authenticated user if exists, otherwise return True for valid service token
            return request.user if hasattr(request, "user") and request.user.is_authenticated else True
        return None


# Create reusable auth instances
service_token_auth = ServiceTokenAuth()

# Combine multiple authentication methods
multi_auth = [service_token_auth, SessionAuth(), x_session_token_auth]
