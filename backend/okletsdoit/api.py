from django.db import router
from ninja import NinjaAPI
from guestlist.api import router as guestlist_router
from core.api import router as core_router
from deadline.api import router as deadline_router
from attachments.api import router as attachments_router
from contacts.api import router as contacts_router
from list.api import router as lists_router

api = NinjaAPI()

api.add_router("/guestlist/", guestlist_router)
api.add_router("/core/", core_router)
api.add_router("/deadline/", deadline_router)
api.add_router("/attachments/", attachments_router)
api.add_router("/contacts/", contacts_router)
api.add_router("/lists/", lists_router)
