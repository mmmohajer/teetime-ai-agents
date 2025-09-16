import json

from websocket.consumers.base import BaseConsumer, BasePrivateConsumer, BasePrivateRoomBasedConsumer

class TestSocketConsumer(BasePrivateRoomBasedConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
               await self._data_handler(text_data)
        except Exception as e:
            print(e)
    
    # --------------------------------------------
    # Data handler Beginning
    # --------------------------------------------
    async def _data_handler(self, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
                task_type = data.get("type") or ""
                await self._send_to_group({
                    "type": "response",
                    "message": f"Received task type: {task_type}",
                    "room": self.room_id
                })
            except json.JSONDecodeError:
                await self._send_to_group({"error": "Invalid JSON format"})
                return
    # --------------------------------------------
    # Data handler Ending
    # --------------------------------------------