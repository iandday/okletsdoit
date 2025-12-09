from ninja import NinjaAPI
from guestlist.api import router as guestlist_router

api = NinjaAPI()

api.add_router("/guestlist/", guestlist_router)
