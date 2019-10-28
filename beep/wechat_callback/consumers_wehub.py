import json
import traceback
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from . import const
from .models import mm_WxUser, mm_WxGroup, mm_WxBot

class WehubConsumer(AsyncWebsocketConsumer):

    logger = logging.getLogger("wehub")

    async def connect(self):
        self.room_name = 'wehub'
        self.room_group_name = 'live_%s' % self.room_name

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

        error_code, error_reason, ack_data, ack_type = self.main_process(wxid, action, req_data_dict)
        ack_dict = {
            'error_code': error_code, 
            'error_reason': error_reason,
            'data': ack_data,
            'ack_type': str(ack_type)
            }
        # 回调wehub
        await self.send(json.dumps(ack_dict))

        # 讲消息转发到对应的群
        if ack_type == 'report_new_msg_ack':
            await self.channel_layer.group_send(
                "live_888",
                {
                    'type': 'wehub_message',
                    'message': json.dumps(req_data_dict)
                }
            )

    def main_req_process(self, wxid, action, request_data_dict):
        self.logger.info("action = {0},data = {1}".format(action, request_data_dict))
        ack_type = 'common_ack'
        if action in const.FIX_REQUEST_TYPES:
            ack_type = str(action)+'_ack'

        if wxid is None or action is None:
            return 1, '参数错误', {}, ack_type
        if action == 'login':
            return 0, "no error", {}, ack_type
        # 更新群成员信息
        # 1. 获取账号的群列表
        # 2. 获取群成员信息

        # 处理获取消息  
        # 根据后台指定的直播群信息进行推送的不同的频道     
        if action == 'report_friend_add_request':
            task_data = {
                'task_type': const.TASK_TYPE_PASS_FRIEND_VERIFY,
                'task_dict': {
                    "v1": request_data_dict.get("v1"),
                    "v2": request_data_dict.get("v2"),
                }
            }
            ack_data_dict = {'reply_task_list': [task_data]}
            return 0, '', ack_data_dict, ack_type
        if action == 'report_new_msg':
            msg_unit = request_data_dict.get('msg', {})
            if msg_unit:
                msg_type = msg_unit.get('msg_type', const.MSG_TYPE_INVALID)
                if msg_type in const.UPLOADFILE_MSG_TYPES:
                    file_index = msg_unit.get('file_index', '')
                    if len(file_index) > 0:
                        task_data = {
                            'task_type': const.TASK_TYPE_UPLOAD_FILE,
                            'task_dict': {
                                'file_index': file_index,
                            }
                        }
                        ack_data_dict = {'reply_task_list': [task_data]}
                        return 0, '', ack_data_dict, ack_type
                elif msg_type == 4902:  # 转账
                    # 这里自动收账
                    transferid = msg_unit.get('transferid', "")
                    wxid_from = msg_unit.get("wxid_from", "")
                    wxid_to = msg_unit.get("wxid_to", "")
                    paysubtype = msg_unit.get("paysubtype", 0)
                    if paysubtype == 1 and wxid_to == wxid:
                        task_data = {
                            'task_type': const.TASK_TYPE_AUTO_ACCOUNT_RECEIVE,
                            'task_dict': {
                                'transferid': transferid,
                                'wxid_from': wxid_from
                            }
                        }
                        self.logger.info("begin auto confirm transferid")
                        ack_data_dict = {'reply_task_list': [task_data]}
                        return 0, '', ack_data_dict, ack_type
                elif msg_type == 1:
                    msg = msg_unit.get("msg", "")
                    room_wxid = msg_unit.get("room_wxid", "")
                    wxid_from = msg_unit.get("wxid_from", "")
                    self.logger.info("recv chatmsg:{0},from:{1}".format(msg, wxid_from))

                    # 测试代码
                    if wxid_from == const.TEST_WXID and msg == str('fqtest'):
                        reply_task_list = []
                        if len(room_wxid) > 0:
                            push_msgunit1 = {
                                'msg_type': const.MSG_TYPE_TEXT,
                                'msg': "群消息自动回复,test\ue537"
                            }

                            push_msgunit2 = {
                                'msg_type': const.MSG_TYPE_IMAGE,
                                'msg': "https://n.sinaimg.cn/mil/transform/500/w300h200/20180917/OBId-hikxxna1858039.jpg"
                            }

                            push_msgunit3 = {
                                'msg_type': const.MSG_TYPE_LINK,
                                'link_url': "http://httpd.apache.org/docs/2.4/getting-started.html",
                                "link_title": "title",
                                "link_desc": "hhhhh_desc",
                                "link_img_url": "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3346649880,432179104&fm=27&gp=0.jpg"
                            }

                            # 自动回复群消息
                            test_task1 = {
                                'task_type': const.TASK_TYPE_SENDMSG,
                                "task_dict":
                                    {
                                        'wxid_to': room_wxid,
                                        'at_list': [wxid_from],
                                        "msg_list": [push_msgunit1, push_msgunit2, push_msgunit3]
                                    }
                            }
                            reply_task_list.append(test_task1)

                        test_task2 = {
                            "task_type": const.TASK_TYPE_SENDMSG,
                            "task_dict":
                                {
                                    "wxid_to": const.TEST_WXID,
                                    "msg_list":
                                        [
                                            {
                                                'msg_type': const.MSG_TYPE_TEXT,
                                                'msg': "wehub文本表情测试,一个商标,一个男人:\ue537\uE138"
                                            },
                                            {
                                                'msg_type': const.MSG_TYPE_TEXT,
                                                'msg': "wehub文本表情测试,一个微笑,一个高尔夫:[微笑]\uE014"
                                            }
                                        ]
                                }
                        }
                        reply_task_list.append(test_task2)
                        ack_data_dict = {
                            'reply_task_list': reply_task_list}
                        return 0, '', ack_data_dict, ack_type

        return 0, 'no error', {}, ack_type

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
            mm_WxUser.update_user(bot_wxid, friend)
        
        # 2. 更新群列表
        group_list = data_dict['group_list']
        my_groups = [group for group in group_list]
        self.room_wxid_list = [group['wxid'] for group in my_groups]
        for group in my_groups:
            mm_WxGroup.update_group(bot_wxid, group)

        # 3. 返回需要上传群信息的群wxid列表
        return self.room_wxid_list

    def process_report_contact_update(self, bot_wxid, data_dict):
        """群成员变化
        https://github.com/tuibao/wehub-callback/blob/master/WeHub%E6%8E%A5%E5%8F%A3%E6%96%87%E6%A1%A3.md#report_contact_update%E4%B8%8A%E6%8A%A5%E6%88%90%E5%91%98%E4%BF%A1%E6%81%AF%E5%8F%98%E5%8C%96
        """
        update_list = data_dict['update_list']
        userinfo_list = []
        groupinfo_list = []
        for info in update_list:
            if 'owner_wxid' not in info:
                userinfo_list.append(info)
            else:
                groupinfo_list.append(info)
        for info in userinfo_list:
            mm_WxUser.update_user(bot_wxid, info)
        for info in groupinfo_list:
            mm_WxGroup.update_group(bot_wxid, info)

    def process_report_room_member_info(self, bot_wxid, data_dict):
        """上报群成员信息
        """
        room_data_list = data_dict['room_data_list']
        for room in room_data_list:
            mm_WxGroup.update_group(bot_wxid, room)

    def process_report_room_member_change(self, bot_wxid, data_dict):
        """上报群成员变化
        """
        pass

    def process_report_new_room(self, bot_wxid, data_dict):
        """上报新群
        """
        
        mm_WxGroup.update_group(bot_wxid, data_dict)

    def process_report_new_msg(self, bot_wxid, data_dict):
        """上报新的聊天消息
        """
        pass

    def main_process(self, wxid, action, request_data_dict):
        self.logger.info("action = {0},data = {1}".format(action, request_data_dict))
        ack_type = 'common_ack'
        if action in const.FIX_REQUEST_TYPES:
            ack_type = str(action)+'_ack'

        if wxid is None or action is None:
            return 1, '参数错误', {}, ack_type
        # 处理微信机器人
        if action == 'login':
            self.process_login(wxid, request_data_dict)

        if action == 'report_contact':
            # 处理群信息
            room_wxid_list = self.process_report_contact(wxid, request_data_dict)
            # 发送上传群成员信息任务
            # room_wxid_list = []
            reply_task_list = []
            task = {
                'task_type': const.TASK_TYPE_REPORT_ROOMMEMBER,
                'task_dict': {
                    'room_wxid_list': room_wxid_list[:5]
                }
            }
            reply_task_list.append(task)
            ack_data = {
                'reply_task_list': reply_task_list
            }
            return 0, "no error", ack_data, ack_type
        
        if action == 'report_contact_update':
            self.process_report_contact_update(wxid, request_data_dict)
            return 0, "no error", {}, ack_type
        
        if action == 'report_room_member_info':
            self.process_report_room_member_info(wxid, request_data_dict)
            return 0, "no error", {}, ack_type

        if action == 'report_new_room':
            self.process_report_new_room(wxid, request_data_dict)

        if action == 'report_room_member_change':
            pass
        if action == 'report_new_msg':
            # 如果是系统消息，则更新群信息
            if 'msg_type' == const.MSG_TYPE_SYSTEM:
                pass

        return 0, 'no error', {}, ack_type