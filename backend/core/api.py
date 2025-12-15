from ninja import Router, Schema
from datetime import date
from typing import Optional

from core.auth import multi_auth
from .models import WeddingSettings

router = Router(tags=["Core"], auth=multi_auth)


# Schemas
class WeddingSettingsSchema(Schema):
    default_data_loaded: bool
    allow_rsvp: bool
    wedding_date: Optional[date] = None
    rsvp_accept_button: str
    rsvp_decline_button: str
    rsvp_attending_label: str
    rsvp_accommodation_label: str
    rsvp_vip_label: str
    rsvp_accept_intro: str
    rsvp_accept_success_message: str
    rsvp_decline_success_message: str
    rsvp_accommodation_intro: str
    rsvp_vip_intro: str
    rsvp_show_accommodation_intro: bool
    rsvp_show_vip_intro: bool
    rsvp_enable_email_updates: bool
    rsvp_email_update_label: str
    rsvp_success_headline: str
    standard_group_label: str
    vip_group_label: str


class WeddingSettingsUpdateSchema(Schema):
    default_data_loaded: Optional[bool] = None
    allow_rsvp: Optional[bool] = None
    wedding_date: Optional[date] = None
    rsvp_accept_button: Optional[str] = None
    rsvp_decline_button: Optional[str] = None
    rsvp_attending_label: Optional[str] = None
    rsvp_accommodation_label: Optional[str] = None
    rsvp_vip_label: Optional[str] = None
    rsvp_accept_intro: Optional[str] = None
    rsvp_accept_success_message: Optional[str] = None
    rsvp_decline_success_message: Optional[str] = None
    rsvp_accommodation_intro: Optional[str] = None
    rsvp_vip_intro: Optional[str] = None
    rsvp_show_accommodation_intro: Optional[bool] = None
    rsvp_show_vip_intro: Optional[bool] = None
    rsvp_enable_email_updates: Optional[bool] = None
    rsvp_email_update_label: Optional[str] = None
    rsvp_success_headline: Optional[str] = None
    standard_group_label: Optional[str] = None
    vip_group_label: Optional[str] = None


# WeddingSettings Endpoints
@router.get("/wedding-settings", response=WeddingSettingsSchema)
def get_wedding_settings(request):
    """Get wedding settings (singleton)"""
    settings = WeddingSettings.load()
    return settings


@router.put("/wedding-settings", response=WeddingSettingsSchema)
def update_wedding_settings(request, payload: WeddingSettingsUpdateSchema):
    """Update wedding settings"""
    settings = WeddingSettings.load()

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(settings, attr, value)

    settings.save()
    return settings
