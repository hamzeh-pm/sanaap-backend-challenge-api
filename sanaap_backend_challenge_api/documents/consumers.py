import json

from channels.generic.websocket import AsyncWebsocketConsumer


class DocumentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("documents", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # cleanup remove channel from group
        await self.channel_layer.group_discard("documents", self.channel_name)

    async def document_created(self, event):
        message = event["data"]["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
