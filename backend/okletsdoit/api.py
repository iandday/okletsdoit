from ninja import NinjaAPI
from guestlist.api import router as guestlist_router
from core.api import router as core_router

api = NinjaAPI()

api.add_router("/guestlist/", guestlist_router)
api.add_router("/core/", core_router)
