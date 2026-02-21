from import_export import resources, fields
from import_export.widgets import BooleanWidget

from .models import Guest, GuestGroup


class YesNoWidget(BooleanWidget):
    """Widget that converts boolean values to Yes/No strings"""

    def render(self, value, obj=None, **kwargs):
        if value is None:
            return ""
        return "Yes" if value else "No"


class GuestResource(resources.ModelResource):
    """Resource for exporting Guest data with related GuestGroup information"""

    group_id = fields.Field(column_name="Group ID", attribute="group__id")
    group_name = fields.Field(column_name="Group Name", attribute="group__name")
    group_email = fields.Field(column_name="Group Email", attribute="group__email")
    group_phone = fields.Field(column_name="Group Phone", attribute="group__phone")
    group_rsvp_code = fields.Field(column_name="Group RSVP Code", attribute="group__rsvp_code")
    group_address_name = fields.Field(column_name="Address Name", attribute="group__address_name")
    group_address = fields.Field(column_name="Address", attribute="group__address")
    group_address_two = fields.Field(column_name="Address 2", attribute="group__address_two")
    group_city = fields.Field(column_name="City", attribute="group__city")
    group_state = fields.Field(column_name="State", attribute="group__state")
    group_zip_code = fields.Field(column_name="ZIP Code", attribute="group__zip_code")
    group_relationship = fields.Field(column_name="Relationship", attribute="group__relationship")
    group_priority = fields.Field(column_name="Priority", attribute="group__priority")
    group_notes = fields.Field(column_name="Group Notes", attribute="group__notes")

    # Use YesNoWidget for boolean fields
    plus_one = fields.Field(column_name="Plus One", attribute="plus_one", widget=YesNoWidget())
    is_invited = fields.Field(column_name="Invited", attribute="is_invited", widget=YesNoWidget())
    is_attending = fields.Field(column_name="Attending", attribute="is_attending", widget=YesNoWidget())
    responded = fields.Field(column_name="Responded", attribute="responded", widget=YesNoWidget())
    accept_accommodation = fields.Field(
        column_name="Accepts Accommodation", attribute="accept_accommodation", widget=YesNoWidget()
    )
    accept_vip = fields.Field(column_name="Accepts VIP", attribute="accept_vip", widget=YesNoWidget())
    accommodation = fields.Field(column_name="Accommodation", attribute="accommodation", widget=YesNoWidget())
    vip = fields.Field(column_name="VIP", attribute="vip", widget=YesNoWidget())
    first_name = fields.Field(column_name="First Name", attribute="first_name")
    last_name = fields.Field(column_name="Last Name", attribute="last_name")

    class Meta:
        model = Guest
        fields = (
            "first_name",
            "last_name",
            "plus_one",
            "notes",
            "group_name",
            "group_email",
            "group_phone",
            "group_rsvp_code",
            "group_address_name",
            "group_address",
            "group_address_two",
            "group_city",
            "group_state",
            "group_zip_code",
            "group_relationship",
            "group_priority",
            "group_notes",
            "is_invited",
            "responded",
            "is_attending",
            "accept_accommodation",
            "accommodation",
            "accept_vip",
            "vip",
        )
        export_order = fields

    def get_queryset(self):
        """Override to filter out deleted guests and prefetch related data"""
        return self.Meta.model.objects.filter(is_deleted=False).select_related("group")


class GuestGroupResource(resources.ModelResource):
    """Resource for exporting GuestGroup data with guest count statistics"""

    # Custom fields for guest counts
    group_count = fields.Field(column_name="Total Guests", attribute="group_count", readonly=True)
    group_standard = fields.Field(column_name="Standard Guests", attribute="group_standard", readonly=True)
    group_vip = fields.Field(column_name="VIP Guests", attribute="group_vip", readonly=True)
    group_overnight = fields.Field(column_name="Accommodation Guests", attribute="group_overnight", readonly=True)
    group_invited_count = fields.Field(column_name="Invited Count", attribute="group_invited_count", readonly=True)
    group_attending_count = fields.Field(
        column_name="Attending Count", attribute="group_attending_count", readonly=True
    )
    group_declined_count = fields.Field(column_name="Declined Count", attribute="group_declined_count", readonly=True)

    # Rename columns for better readability
    name = fields.Field(column_name="Group Name", attribute="name")
    address_name = fields.Field(column_name="Address Name", attribute="address_name")
    email = fields.Field(column_name="Email", attribute="email")
    phone = fields.Field(column_name="Phone", attribute="phone")
    address = fields.Field(column_name="Address", attribute="address")
    address_two = fields.Field(column_name="Address 2", attribute="address_two")
    city = fields.Field(column_name="City", attribute="city")
    state = fields.Field(column_name="State", attribute="state")
    zip_code = fields.Field(column_name="ZIP Code", attribute="zip_code")
    relationship = fields.Field(column_name="Relationship", attribute="relationship")
    priority = fields.Field(column_name="Priority", attribute="priority")
    rsvp_code = fields.Field(column_name="RSVP Code", attribute="rsvp_code")
    notes = fields.Field(column_name="Notes", attribute="notes")

    class Meta:
        model = GuestGroup
        fields = (
            # Basic info
            "name",
            "email",
            "phone",
            "rsvp_code",
            # Address
            "address_name",
            "address",
            "address_two",
            "city",
            "state",
            "zip_code",
            # Group details
            "relationship",
            "priority",
            "notes",
            # Statistics
            "group_count",
            "group_standard",
            "group_vip",
            "group_overnight",
            "group_invited_count",
            "group_attending_count",
            "group_declined_count",
        )
        export_order = fields

    def get_queryset(self):
        """Override to filter out deleted groups and prefetch guests"""
        return self.Meta.model.objects.filter(is_deleted=False).prefetch_related("guests")
