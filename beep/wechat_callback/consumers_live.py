from channels.auth import login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .models import mm_WxUser

"""消息格式
msg_type
1: 弹幕
2：微信消息

{
    "msg_type": "聊天消息| 弹幕",
    "msg_dict": {

    },
    "user": { 
        "id": "",
        "name": "",
        "avatar": "",
    }
        
}
"""

class LiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.user = self.scope["user"]
        # await login(self.scope, user)
        # await database_sync_to_async(self.scope["session"].save)()
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        message = json.loads(text_data)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = {
            'id': self.user.id,
            'name': self.user.name,
            'avatar_url': self.user.avatar_url,
            'user_type': 'user'
        }
        user_message = {
            'msg_type': 'user',
            'msg_dict': message,
            'user': user
        }
        # Send message to WebSocket
        await self.send(text_data=json.dumps(user_message))

    # Receive message from room group
    async def wehub_message(self, event):
        message = event['message']
        wxid = message['wxid_from']
        user = await database_sync_to_async(mm_WxUser.get_info)(wxid)
        text_dict = {
            'msg_type': 'wechat',
            'msg_dict': message,
            'user': user
        }
        await self.send(json.dumps(text_dict))