from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PhotoUpdatesConsumer(AsyncJsonWebsocketConsumer):
    group_name = "photos"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def photo_update(self, event):
        await self.send_json(
            {
                "event": event.get("event", "photo.updated"),
                "photoId": event.get("photo_id"),
                "status": event.get("status"),
                "uploadedAt": event.get("uploaded_at"),
            }
        )
