from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    """
    Render the main page of the application.
    """
    return render(request, "core/index.html")


def venue(request):
    """
    Render the venues page of the application.
    """
    return render(request, "core/venue.html")


def our_story(request):
    """
    Render the 'Our Story' page of the application.
    """
    return render(request, "core/our_story.html")


def rsvp(request):
    """
    Render the 'RSVP' page of the application.
    """
    return render(request, "core/rsvp.html")


def photos(request):
    """
    Render the 'Photos' page of the application.
    """
    return render(request, "core/photos.html")
