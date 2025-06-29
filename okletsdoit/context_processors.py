def site_vars(request):
    return {
        "site_title": "Steph & Ian",
        "logo": "static/images/logo.png",
        "nav_links": [
            {"view_name": "our_story", "icon": "fa-cubes", "text": "Our Story"},
            {"view_name": "venue", "icon": "fa-cubes", "text": "Venue"},
            {"view_name": "home", "icon": "fa-list", "text": "Photos"},
            {"view_name": "home", "icon": "fa-list", "text": "RSVP"},
        ],
        "sidebar_app_links": [
            {"view_name": "settings", "icon": "fa-gear", "text": "Settings"},
            {"view_name": "account_logout", "icon": "fa-sign-out", "text": "Logout"},
        ],
    }
