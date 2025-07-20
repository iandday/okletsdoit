from datetime import datetime

from urllib.parse import quote as urllib_quote


def site_vars(request):
    address = "16187 Kreashbaum Road"
    city = "Rockbridge"
    state = "OH"
    zipcode = "43149"

    return {
        "site_title": "Steph & Ian",
        "logo": "static/images/logo.png",
        "wedding_data": {
            "date": "2026-11-07",
            "time": "18:00:00",
            "location": "Timberframe Lodge",
            "address": address,
            "city": city,
            "state": state,
            "zip": zipcode,
            "google_maps_url": f"https://maps.google.com/?q={urllib_quote(f'{address},{city},{state},{zipcode}')}",
            "apple_maps_url": f"https://maps.apple.com/?address={urllib_quote(f'{address},{city},{state},{zipcode}')}",
            "rsvp_deadline": "2024-04-30",
            "schedule": [
                {
                    "start_time": datetime.strptime("18:00:00", "%H:%M:%S").time(),
                    "end_time": datetime.strptime("18:30:00", "%H:%M:%S").time(),
                    "event": "Ceremony",
                    "description": "Join us for the wedding ceremony.",
                },
                {
                    "start_time": datetime.strptime("19:00:00", "%H:%M:%S").time(),
                    "end_time": datetime.strptime("20:00:00", "%H:%M:%S").time(),
                    "event": "Cocktail Hour",
                    "description": "Enjoy drinks and appetizers.",
                },
                {
                    "start_time": datetime.strptime("20:00:00", "%H:%M:%S").time(),
                    "end_time": datetime.strptime("21:00:00", "%H:%M:%S").time(),
                    "event": "Photos",
                    "description": "Capture memories with the couple.",
                },
                {
                    "start_time": datetime.strptime("20:00:00", "%H:%M:%S").time(),
                    "end_time": datetime.strptime("23:00:00", "%H:%M:%S").time(),
                    "event": "Reception",
                    "description": "Dinner and activities to follow.",
                },
            ],
        },
        "lodging_info": [
            {
                "name": "Holiday Inn Express Hocking Hills",
                "address": "12916 Grey St, Logan, OH 43138",
                "phone": "740-385-7700",
                "website": "https://www.ihg.com/holidayinnexpress/hotels/us/en/logan/loaoh/hoteldetail?cm_mmc=GoogleMaps-_-EX-_-US-_-LOAOH",
                "description": "Located about 20 minutes from the venue, this hotel offers modern amenities and a complimentary breakfast.",
            },
            {
                "name": "Sleep Inn Logan Ohio-Hocking Hills",
                "address": "12830 Grey Street, Logan, OH 43138",
                "phone": "740-279-1258",
                "website": "https://www.choicehotels.com/ohio/logan/sleep-inn-hotels/oh706?mc=llgoxxpx",
                "description": "This hotel offers comfortable rooms and is located about 20 minutes from the venue.",
            },
            {
                "name": "VRBO",
                "address": None,
                "phone": None,
                "website": "https://www.vrbo.com/search?destination=16187%20Kreashbaum%20Rd%2C%20Rockbridge%2C%20OH%2043149%2C%20USA&flexibility=1_DAY&searchRange=2026-06-01_2026-06-30&adults=2&sort=RECOMMENDED&upsellingNumNightsAdded=&theme=&userIntent=&semdtl=&upsellingDiscountTypeAdded=&categorySearch=",
                "description": "Find a cozy cabin or home rental in the Hocking Hills area.",
            },
            {
                "name": "Airbnb",
                "address": None,
                "phone": None,
                "website": "https://www.airbnb.com/s/16187-Kreashbaum-Road--Rockbridge--OH/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJDzcrPaHsR4gR1pkhZtsMNoY&adults=1",
                "description": "Find a cozy cabin or home rental in the Hocking Hills area.",
            },
            {
                "name": "Top O' The Caves Campground",
                "address": "26780 Chapel Ridge Rd, South Bloomingville, OH 43152",
                "phone": "740-385-6566",
                "website": "https://www.campspot.com/park/top-o-the-caves-campground",
                "description": "Offers camping sites and cabin rentals in the Hocking Hills area.",
            },
            {
                "name": "Campbell Cove Campground by Lake Logan",
                "address": "30713 Lake Logan Rd, Logan, OH 43138",
                "phone": "740-205-2024",
                "website": "https://www.campbellcovecampgrounds.com/",
                "description": "Offers full hook up RV sites, camping cabins and tent sites.",
            },
        ],
        "local_attractions": [
            {
                "name": "Hocking Hills State Park",
                "description": "A beautiful state park known for its stunning landscapes, hiking trails, and waterfalls.",
                "url": "https://www.hockinghills.com/state_parks/hocking_hills_state_park.html",
                "image_url": "https://innatcedarfalls.com/wp-content/uploads/2024/05/GettyImages-820732146copy.jpg",
                "previous_index": 4,
                "next_index": 2,
            },
            {
                "name": "Hocking Hills Winery",
                "description": "A charming winery offering tastings and beautiful views of the Hocking Hills.",
                "url": "https://www.hockinghillswinery.com/",
                "image_url": "https://lirp.cdn-website.com/ea63b10e/dms3rep/multi/opt/IMG_1093-97c1078e-1920w.jpeg",
                "previous_index": 1,
                "next_index": 3,
            },
            {
                "name": "Ash Cave",
                "description": "The largest recess cave in Ohio, offering a picturesque waterfall and scenic views.",
                "url": "https://www.hockinghills.com/state_parks/ash_cave.html",
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWKQalQkX3jmfE68gh-Yzg5-jVrtJyKsE5xQ&s",
                "previous_index": 2,
                "next_index": 4,
            },
            {
                "name": "Old Man's Cave",
                "description": "A popular hiking destination featuring unique rock formations and lush forests.",
                "url": "https://www.hockinghills.com/state_parks/old_mans_cave.html",
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbyTLop2RroJGu57EckX6DJ8wceiqKDhwac3QPhWLNkzeiZqAceAM0RAnp8nTiML0uBy0&usqp=CAU",
                "previous_index": 3,
                "next_index": 1,
            },
        ],
        "nav_links": [
            {"view_name": "core:our_story", "icon": "fa-heart", "text": "Our Story"},
            {"view_name": "core:venue", "icon": "fa-hotel", "text": "Venue"},
            {"view_name": "core:photos", "icon": "fa-camera", "text": "Upload Photos"},
            {"view_name": "core:rsvp", "icon": "fa-pen-to-square", "text": "RSVP"},
        ],
        "planning_links": [
            {"view_name": "deadline:deadline_summary", "icon": "fa-list", "text": "Deadlines"},
            {"view_name": "core:idea_list", "icon": "fa-lightbulb", "text": "Ideas"},
            {"view_name": "expenses:summary", "icon": "fa-dollar-sign", "text": "Budget"},
            {"view_name": "contacts:list", "icon": "fa-address-book", "text": "Contacts"},
            {"view_name": "list:summary", "icon": "fa-list-check", "text": "Lists"},
        ],
        "sidebar_app_links": [
            {"view_name": "settings", "icon": "fa-gear", "text": "Settings"},
            {"view_name": "account_logout", "icon": "fa-sign-out", "text": "Logout"},
        ],
    }
