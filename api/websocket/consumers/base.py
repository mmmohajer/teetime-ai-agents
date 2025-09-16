from django.core.cache import cache
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import functools
import asyncio
from rest_framework_simplejwt.tokens import AccessToken
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async

from core.models import UserModel, ProfileModel

class BaseConsumer(AsyncWebsocketConsumer):

    async def _send_json(self, data):
        await self.send(text_data=json.dumps(data))

    async def _send_bytes(self, data):
        await self.send(bytes_data=data)
    
    async def _run_blocking(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))
    
    async def _handle_error(self, message):
        return await self._send_json({"error": message, "remove_loader": True})
    
    async def connect(self):
        await self.accept()
        return await self._send_json({
            "connection": True
        })

    async def disconnect(self, close_code):
        return await self._send_json({
            "connection": False
        })

class BasePrivateConsumer(BaseConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = None
    
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        token = parse_qs(query_string).get('token', [None])[0]
        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                self.profile = await sync_to_async(
                    lambda: ProfileModel.objects.select_related("user").get(user_id=user_id)
                )()
                await self.accept()
                await self._send_json({
                    "connection": True,
                    "email": self.profile.user.email
                })
            except Exception as e:
                await self._send_json({
                    "connection": False,
                })
                return await self._handle_error(f"{e}")
            
class BasePrivateRoomBasedConsumer(BasePrivateConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = ""


    async def connect(self):
        await super().connect()
        self.room_id = self.scope["url_route"]["kwargs"].get("room_id")
        if not self.profile or not self.room_id:
            await self._send_json({"connection": False})
            return await self._handle_error("Missing user or room id.")
        allowed = await self._can_user_join_room()
        if allowed:
            await self.channel_layer.group_add(self._room_group_name(), self.channel_name)
            await self._send_json({
                "connection": True,
            })
            cache_key = f"room_{self.room_id}_members"
            group_members = cache.get(cache_key, [])
            if self.profile.user.email not in group_members:
                group_members.append(self.profile.user.email)
                cache.set(cache_key, group_members, None)
            members = [user for user in group_members]
            await self._send_to_group({
                "members": members,
            })
        else:
            await self._send_json({"connection": False})
            return await self._handle_error("Access denied to this room.")

    async def disconnect(self, close_code):
        if self.room_id:
            await self.channel_layer.group_discard(self._room_group_name(), self.channel_name)
            cache_key = f"room_{self.room_id}_members"
            group_members = cache.get(cache_key, [])
            if self.profile and self.profile.user.email in group_members:
                group_members.remove(self.profile.user.email)
                cache.set(cache_key, group_members, None)
                await self._send_to_group({"members": group_members})
        await super().disconnect(close_code)


    async def _send_to_group(self, data, event_type="broadcast_message"):
        """
        Broadcast any JSON-serializable data to all users in the room group.
        event_type: the Channels handler name (default: broadcast_message)
        """
        event = {"type": event_type}
        event.update(data)
        await self.channel_layer.group_send(
            self._room_group_name(),
            event
        )
    
    async def _can_user_join_room(self):
        return True
    
    async def broadcast_message(self, event):
        data = {k: v for k, v in event.items() if k != "type"}
        await self._send_json(data)

    def _room_group_name(self):
        return f"room_{self.room_id}"