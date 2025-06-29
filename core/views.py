from django.shortcuts import render

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
