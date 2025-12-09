from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin
    from django.http import HttpRequest

    from users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return settings.ACCOUNT_ALLOW_REGISTRATION


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_SOCIAL_REGISTRATION", True)

    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, typing.Any],
    ) -> User:
        """
        Populates user information from social provider info.

        See: https://docs.allauth.org/en/latest/socialaccount/advanced.html#creating-and-populating-user-instances
        """
        user = sociallogin.user
        # Extract full name from OIDC data (adjust 'name' based on your OIDC provider's claims)
        full_name = data.get("name")
        if full_name:
            parts = full_name.split(" ", 1)  # Split into at most two parts
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        # You can also handle other fields here if needed
        return user

    def get_login_redirect_url(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
    ) -> str:
        """
        Returns the redirect URL after successful social login.

        This method checks for a 'redirect' parameter in the request's GET parameters
        and uses it as the redirect URL if present. Otherwise, it falls back to the
        default behavior.
        """
        redirect_url = request.GET.get("redirect")
        if redirect_url:
            return redirect_url
        return super().get_login_redirect_url(request, sociallogin)
