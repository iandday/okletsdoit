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
            {"view_name": "core:home", "icon": "fa-house", "text": "Home"},
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
            {"view_name": "guestlist:guestlist_summary", "icon": "fa-users", "text": "Guest List"},
            {"view_name": "core:timeline_summary", "icon": "fa-users", "text": "Timeline"},
        ],
        "sidebar_app_links": [
            {"view_name": "settings", "icon": "fa-gear", "text": "Settings"},
            {"view_name": "account_logout", "icon": "fa-sign-out", "text": "Logout"},
        ],
        "our_story": [
            {
                "title": "The Match",
                "svg": "M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z",
                "content": [
                    "It all started with a swipe right on Hinge. Two people on opposite sides of Columbus, both more than a little skeptical of online dating but still hoping to find something real. Neither of us expected much, but here we are."
                ],
            },
            {
                "title": "Let's Set The Scene",
                "svg": "M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.478 8-10 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.478-8 10-8s10 3.582 10 8z",
                "content": [
                    "Ian had just sold his house and was getting ready to spend a month in Delaware, the state for all you Ohioans, before moving into a new place in Columbus. Steph debated saying yes to the date; she was convinced she’d catch feelings and then Ian would decide to stay in Delaware permanently. But she said yes anyway."
                ],
            },
            {
                "title": "The First Date Blunder",
                "svg": "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.99-.833-2.76 0L4.054 15.5c-.77.833.192 2.5 1.732 2.5z",
                "content": [
                    "Steph picked the place, a bar in Easton called The Beeline, not knowing that Ian lived across town, all the way in Galloway. Obviously she beat him there! So, she waited and waited and waited.",
                    'When Ian finally strolled up, he skipped the small talk and opened with, "Huh. I thought your hair would be brighter."',
                    "The audacity of this man, we hadn’t even walked inside yet! Surprisingly, Steph laughed it off and didn’t toss a drink in his face later. And that’s when Ian knew he’d said something dumb, but maybe to the right person.",
                ],
            },
            {
                "title": "The Rest is History",
                "svg": "M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z",
                "content": [
                    "From that slightly awkward start to the first date, our love story unfolded. Believe it or not, Ian didn’t ghost Steph and came back to Columbus! And they continued seeing each other and definitely caught feelings.",
                    "After countless dates and memories, tons of laughs, adventures, and concerts, and of course, lots of sarcastic comments and jests along the way, we discovered that sometimes the best relationships start with somewhat cringe-worthy moments.",
                    "Who knew that insulting someone's hair on a first date could be the foundation of forever? Ian certainly didn't! Yet here we are, planning our wedding and proving that love truly does find a way, even when you start with the world's worst opening line.",
                ],
            },
        ],
        "call_to_action": {
            "our_story": "We can't wait to celebrate with you as we turn this beautiful, chaotic love story into marriage.  And don't worry - Ian promises not to comment on anyone's hair at the wedding."
        },
    }
