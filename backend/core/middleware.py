"""
Custom middleware for handling service-to-service communication
"""

from django.conf import settings


class ServiceTokenSecurityMiddleware:
    """
    Middleware to bypass HTTPS redirect for service token authenticated requests.
    This allows internal Docker container-to-container communication over HTTP
    while maintaining HTTPS for external requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if request required token for backend service communication
        service_token = request.headers.get("X-Service-Token")
        if service_token and service_token == settings.SERVICE_TOKEN:
            request._is_service_request = True

        return self.get_response(request)
