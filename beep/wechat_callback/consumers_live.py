from channels.generic.websocket import AsyncWebsocketConsumer
import json

"""消息格式
msg_type
1: 弹幕
2：微信消息

{
    "msg_type": "聊天消息| 弹幕",
    "msg": {
        "txt": "xxxxx"
    },
    "msg_wechat": {}
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
        user_message = {
            'msg_type': 'user',
            'msg_dict': message,
            'user': {}
        }
        # Send message to WebSocket
        await self.send(text_data=json.dumps(user_message))

    # Receive message from room group
    async def wehub_message(self, event):
        message = event['message']
        text_dict = {
            'msg_type': 'wechat',
            'msg_dict': message,
            'user': {}
        }
        await self.send(json.dumps(text_dict))