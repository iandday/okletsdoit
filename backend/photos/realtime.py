from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def publish_photo_update(*, event: str, photo_id: str, status: str, uploaded_at: str | None = None) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        "photos",
        {
            "type": "photo_update",
            "event": event,
            "photo_id": photo_id,
            "status": status,
            "uploaded_at": uploaded_at,
        },
    )
