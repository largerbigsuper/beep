import json
import traceback
import logging
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from . import const
from .models import mm_WxUser, mm_WxGroup, mm_WxBot, mm_WxMessage


class WehubTaskConsumer(AsyncWebsocketConsumer):

    logger = logging.getLogger("wehub_task")

    async def connect(self):
        self.room_name = 'wehub_task'
        self.room_group_name = self.room_name
        self.logger.info('WebSocket CONNECT {} {}'.format(self.scope['path'], self.scope['client']))
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
        self.logger.info('WebSocket DISCONNECT {} {}'.format(self.scope['path'], self.scope['client']))

    # Receive message from WebSocket
    async def receive(self, text_data):
        message = text_data
        self.logger.info('raw data: {}'.format(message))
        try:
            if message:
                ack_dict = json.loads(str(message), strict=False)
                await self.channel_layer.group_send(
                    'wehub',
                    {
                        'type': 'wehub_task',
                        'message': ack_dict,
                    }
                )

        except Exception as e:
            self.logger.error(
                "exception occur: {}".format(traceback.format_exc()))
            return

