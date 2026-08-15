from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def clear_csrf_and_force_login(request, reason=""):
    logout(request)
    response = HttpResponseRedirect(reverse("account_login"))
    response.delete_cookie("csrftoken")
    response.delete_cookie("sessionid")
    return response
