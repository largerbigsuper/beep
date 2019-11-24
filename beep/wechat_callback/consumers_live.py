import time

from channels.auth import login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .models import mm_WxUser, mm_WxMessage

"""消息格式
msg_type
admin: 系统消息
user：普通消息
wechat：微信消息

{
    "msg_type": "",
    "msg_dict": {
        "msg": "消息text",
        "msg_type": 0 # 0：普通消息 1:提问
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
        """处理用户发送的消息
        """
        message = json.loads(text_data)
        msg_type = 'admin'
        if self.user.is_authenticated:
            user = {
                'id': self.user.id,
                'name': self.user.name,
                'avatar_url': self.user.avatar_url_url,
                'user_type': 1
            }
            msg_type = 'user'
        else:
            user = {
                'id': 0,
                'name': '系统消息',
                'avatar_url': '',
                'user_type': 2
            }
            
        user_message = {
            'msg_type': msg_type,
            'msg_dict': message,
            'user': user
        }

        room_wxid = self.room_name + '@chatroom'
        # 群发
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': user_message
            }
        )
        
        # 提问需要推送到wehub
        # 普通聊天为 0
        # 提问消息类型为 1
        user_msg_type = message.get('msg_type', 0)
        if user_msg_type == 1:
            await self.channel_layer.group_send(
                'wehub',
                {
                    'type': 'live_message',
                    'message': user_message,
                    'room_wxid': room_wxid
                }
            )

        # 记录
        # '10000' 普通聊天消息， '10001' 提问消息
        saved_msg_type = '10000'
        if user_msg_type == 1:
            saved_msg_type = '10001'
        wxmessage_dict = {
            'user_type': user['user_type'],
            'user_id': user['id'],
            'msg': message['msg'],
            'raw_msg': message,
            'room_wxid': room_wxid,
            'wxid_from': str(self.user.id),
            'wxid_to': room_wxid,
            'msg_timestamp': int(round(time.time() * 1000)),
            'msg_type': saved_msg_type
        }

        await  database_sync_to_async(mm_WxMessage.create)(**wxmessage_dict)

    # Receive message from room group
    async def chat_message(self, event):
        # 处理每个socket链接的函数， self.scope['user'] 是每个socket链接对应的user
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

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