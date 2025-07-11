def site_vars(request):
    return {
        "site_title": "Steph & Ian",
        "logo": "static/images/logo.png",
        "wedding_data": {
            "date": "2026-11-07",
            "time": "18:00:00",
            "location": "The Grand Hall",
            "address": "123 Celebration Ave, Cityville",
            "rsvp_deadline": "2024-04-30",
        },
        "nav_links": [
            {"view_name": "core:our_story", "icon": "fa-heart", "text": "Our Story"},
            {"view_name": "core:venue", "icon": "fa-hotel", "text": "Venue"},
            {"view_name": "core:photos", "icon": "fa-camera", "text": "Upload Photos"},
            {"view_name": "core:rsvp", "icon": "fa-pen-to-square", "text": "RSVP"},
        ],
        "planning_links": [
            {"view_name": "core:task_list", "icon": "fa-list", "text": "Deadlines"},
            {"view_name": "core:idea_list", "icon": "fa-lightbulb", "text": "Ideas"},
        ],
        "sidebar_app_links": [
            {"view_name": "settings", "icon": "fa-gear", "text": "Settings"},
            {"view_name": "account_logout", "icon": "fa-sign-out", "text": "Logout"},
        ],
    }
