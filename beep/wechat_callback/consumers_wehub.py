import json
import traceback
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from . import const
from .models import mm_WxUser, mm_WxGroup, mm_WxBot, mm_WxMessage
from .tasks import update_or_create_wxuser, update_or_create_wxgroup


class WehubConsumer(AsyncWebsocketConsumer):

    logger = logging.getLogger("wehub")

    async def connect(self):
        self.room_name = 'wehub'
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
                request_dict = json.loads(str(message), strict=False)
                await self.process_commond(request_dict)

        except Exception as e:
            self.logger.error(
                "exception occur: {}".format(traceback.format_exc()))
            return

    async def process_commond(self, request_dict):
        # 处理wehub客户端程序发过来的消息
        appid = request_dict.get('appid', None)
        action = request_dict.get('action', None)
        wxid = request_dict.get('wxid', None)
        req_data_dict = request_dict.get('data', {})

        if appid is None or action is None or wxid is None:
            self.logger.info("invalid param")
            return

        save_msg = False
        if action == 'report_new_msg':
            msg_dict = req_data_dict['msg']
            room_wxid = msg_dict.get('room_wxid')
            live_rooms = mm_WxUser.cache.get(mm_WxUser.key_live_rooms, set())
            if room_wxid in live_rooms:
                save_msg = True

        error_code, error_reason, ack_data, ack_type = self.main_process(wxid, action, req_data_dict, save_msg)
        ack_dict = {
            'error_code': error_code,
            'error_reason': error_reason,
            'data': ack_data,
            'ack_type': str(ack_type)
        }
        # 回调wehub
        ack_data_text = json.dumps(ack_dict)
        self.logger.info('===ack_data==: {}'.format(ack_data_text))
        await self.send(ack_data_text)

        # 讲消息转发到对应的群
        if save_msg and action == 'report_new_msg':
            msg_dict = req_data_dict['msg']
            room_wxid = msg_dict.get('room_wxid')
            if room_wxid:
                channel_name = room_wxid.replace('@chatroom', '')
                await self.channel_layer.group_send(
                    channel_name,
                    {
                        'type': 'wehub_message',
                        'message': msg_dict
                    }
                )
        # 更新群成员变化
        elif action == 'report_room_member_change':
            # 发送上传群成员信息任务
            wxid_list = []
            if req_data_dict['flag']:
                wxid_list = req_data_dict['wxid_list']
            ack_type = 'common_ack'
            for wxid in wxid_list:
                reply_task_list = []
                task = {
                    'task_type': const.TASK_TYPE_REPORT_USER_INFO,
                    'task_dict': {
                        'wxid': wxid
                    }
                }
                reply_task_list.append(task)
                ack_data = {
                    'reply_task_list': reply_task_list
                }
                ack_dict = {
                    'error_code': 0,
                    'error_reason': "no error",
                    'data': ack_data,
                    'ack_type': ack_type
                }
                # 回调wehub
                ack_data_text = json.dumps(ack_dict)
                self.logger.info('===ack_data==: {}'.format(ack_data_text))
                await self.send(ack_data_text)

    def process_login(self, wxid, data_dict):
        """微信机器人
        """

        mm_WxBot.update_bot(wxid=wxid, data=data_dict)

    def process_report_contact(self, bot_wxid, data_dict):
        """上报好友与群列表
        """
        # 1. 更新好友列表
        friend_list = data_dict['friend_list']
        for friend in friend_list:
            # mm_WxUser.update_user(friend)
            update_or_create_wxuser.delay(friend)

        # 2. 更新群列表
        group_list = data_dict['group_list']
        my_groups = [group for group in group_list]

        for group in my_groups:
            # mm_WxGroup.update_group(bot_wxid, group)
            update_or_create_wxgroup.delay(bot_wxid, group)

        # 3. 返回需要上传群信息的群wxid列表
        # 去除已经同步的群
        # saved_groups = set(mm_WxGroup.all().values_list('room_wxid', flat=True))
        # room_wxid_list = [group['wxid'] for group in my_groups if group['wxid'] not in saved_groups]
        room_wxid_list = [group['wxid'] for group in my_groups]
        
        return room_wxid_list

    def process_report_contact_update(self, bot_wxid, data_dict):
        """群成员变化
        https://github.com/tuibao/wehub-callback/blob/master/WeHub%E6%8E%A5%E5%8F%A3%E6%96%87%E6%A1%A3.md#report_contact_update%E4%B8%8A%E6%8A%A5%E6%88%90%E5%91%98%E4%BF%A1%E6%81%AF%E5%8F%98%E5%8C%96
        """
        update_list = data_dict['update_list']
        userinfo_list = []
        groupinfo_list = []
        for info in update_list:
            wxid = info['wxid']
            if wxid.endswith('chatroom'):
                groupinfo_list.append(info)
            else:
                userinfo_list.append(info)
        for info in userinfo_list:
            # mm_WxUser.update_user(info)
            update_or_create_wxuser.delay(info)
        for info in groupinfo_list:
            # mm_WxGroup.update_group(bot_wxid, info)
            update_or_create_wxgroup.delay(bot_wxid, info)

    def process_report_room_member_info(self, bot_wxid, data_dict):
        """上报群成员信息
        """
        room_data_list = data_dict['room_data_list']
        for room in room_data_list:
            # mm_WxGroup.update_group(bot_wxid, room)
            update_or_create_wxgroup.delay(bot_wxid, room)
            memberInfo_list = room['memberInfo_list']
            for info in memberInfo_list:
                info.pop('room_nickname')
                # mm_WxUser.update_user(info)
                update_or_create_wxuser.delay(info)

    def process_report_room_member_change(self, bot_wxid, data_dict):
        """上报群成员变化
        request
        {
            "action":"report_room_member_change",
            "appid":"xxxxxxx",
            "wxid": "wxid_xxxxxxx",
            "data":{
                "room_wxid":"xxxxxxx@chatroom",
                "owner_wxid":"xxxxx",	//群主wxid, 0.3.8版本中加入
                "wxid_list";["xxxxxx","xxxxx"],  //变化的成员的wxid列表
                "flag": flag //0,群成员减少;1,群成员增加
            }
        }
        {
            "action":"report_room_member_change",
            "appid":"xxxxxxx",
            "wxid": "wxid_xxxxxxx",
            "data":{
                "room_wxid":"21746845232@chatroom",
                "owner_wxid":"yueguixiang888",
                "wxid_list":["wxid_motqmk6dfsd122"],  
                "flag": 1
            }
        }
        """
        pass

    def process_report_new_room(self, bot_wxid, data_dict):
        """上报新群
        """

        mm_WxGroup.update_group(bot_wxid, data_dict)

    def process_report_new_msg(self, bot_wxid, data_dict):
        """上报新的聊天消息
        """
        # 存储消息
        wxmessage_dict = data_dict['msg']
        mm_WxMessage.create(bot_wxid=bot_wxid, **wxmessage_dict)

    def process_report_user_info(self, bot_wxid, data_dict):
        """上报具体某个微信的详情 request格式
        {
        "action":"report_user_info",
        "appid": "xxxxxxx",         
        "wxid" : "wxid_xxxxxxxx"
        "data":
        {
            "wxid":  "xxxxx",               //wxid
            "wx_alias": "xxxxx",            //有可能为空
            "nickname":"xxxxx",             //微信昵称
            "remark_name" :"xxxx",          //好友备注
            "head_img":"http://xxxxxxxx"    //头像的url地址(有可能获取不到为空)
            "head_img_data":"xxxxxxxxxx"    //头像的二进制数据(jpg格式)经过base64编码后的字符串
            "sex" : xx ,            //性别:0未知,1 男， 2 女
            "country":"xxx",        //祖国(可能为空)
            "province":"xxxx",      //省份(可能为空)
            "city":"xxxxx"          //城市(可能为空)
            "is_friend": x              //是否是我的好友,0:不是;1:是
            "room_list":["xx","xxx"]    //该微信号所在的群的列表
        }
        }
        """
        mm_WxUser.update_user(data_dict)

    def main_process(self, wxid, action, request_data_dict, save_msg):
        # self.logger.info("action = {0},data = {1}".format(
        #     action, request_data_dict))
        ack_type = 'common_ack'
        if action in const.FIX_REQUEST_TYPES:
            ack_type = str(action)+'_ack'

        if wxid is None or action is None:
            return 1, '参数错误', {}, ack_type

        # 处理微信机器人
        if action == 'login':
            self.process_login(wxid, request_data_dict)

        elif action == 'report_contact':
            # 处理群信息
            room_wxid_list = self.process_report_contact(wxid, request_data_dict)
            # 发送上传群成员信息任务
            # room_wxid_list = []
            reply_task_list = []
            task = {
                'task_type': const.TASK_TYPE_REPORT_ROOMMEMBER,
                'task_dict': {
                    'room_wxid_list': room_wxid_list
                }
            }
            reply_task_list.append(task)
            ack_data = {
                'reply_task_list': reply_task_list
            }
            return 0, "no error", ack_data, ack_type

        elif action == 'report_contact_update':
            self.process_report_contact_update(wxid, request_data_dict)

        elif action == 'report_room_member_info':
            self.process_report_room_member_info(wxid, request_data_dict)

        elif action == 'report_new_room':
            self.process_report_new_room(wxid, request_data_dict)

        elif action == 'report_room_member_change':
            pass

        elif action == 'report_user_info':
            self.process_report_user_info(wxid, request_data_dict)

        elif action == 'report_new_msg':
            if save_msg:
                # 如果是系统消息，则更新群信息
                self.process_report_new_msg(wxid, request_data_dict)
                # 处理文件回调
                msg_dict = request_data_dict['msg']
                msg_type = msg_dict['msg_type']
                if msg_type in [const.MSG_TYPE_IMAGE, const.MSG_TYPE_VOICE]:
                    reply_task_list = []
                    task = {
                        'task_type': const.TASK_TYPE_UPLOAD_FILE,
                        'task_dict': {
                            'file_index': msg_dict['file_index']
                        }
                    }
                    reply_task_list.append(task)
                    ack_data = {
                        'reply_task_list': reply_task_list
                    }
                    return 0, 'no error', ack_data, ack_type
        else:
            pass
        return 0, 'no error', {}, ack_type

    async def live_message(self, event):
        """发送消息到wehub
        """
        user_message = event['message']
        user = user_message['user']
        message = user_message['msg_dict']
        room_wxid = event['room_wxid']
        reply_task_list = []
        msg_unit = {
            'msg_type': 1,
            'msg': '来自Beep的[' + user['name'] + ']: ' + message['msg']
        }
        task = {
            'task_type': const.TASK_TYPE_SENDMSG,
            'task_dict': {
                'wxid_to': room_wxid,
                'at_list': [],
                'msg_list': [msg_unit],
                'at_style': 0
            }
        }
        reply_task_list.append(task)
        ack_data = {
            'reply_task_list': reply_task_list
        }
        ack_dict = {
            'error_code': 0,
            'error_reason': "no error",
            'data': ack_data,
            'ack_type': 'common_ack'
        }
        # 回调wehub
        await self.send(json.dumps(ack_dict))

    async def wehub_task(self, event):
        """自定义命令
        """
        ack_dict = event['message']
        for f in ['error_code', 'error_reason', 'data', 'ack_type']:
            if f not in ack_dict:
                return
        
        await self.send(json.dumps(ack_dict))
