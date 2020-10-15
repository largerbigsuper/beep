from celery import shared_task

from .models import mm_WxUser, mm_WxGroup, mm_WxBot, mm_WxMessage

@shared_task
def update_or_create_wxbot(wxid, botinfo_dict):
    """更新机器人账号信息
    """
    mm_WxBot.update_bot(wxid=wxid, data=botinfo_dict)

@shared_task
def update_or_create_wxuser(userinfo_dict):
    """更新微信用户
    """
    mm_WxUser.update_user(userinfo_dict)


@shared_task
def update_or_create_wxgroup(bot_wxid, groupinfo_dict):
    """更新微信群信息
    """
    mm_WxGroup.update_group(bot_wxid, groupinfo_dict)


@shared_task
def save_wxmessage(bot_wxid, wxmessage_dict):
    """保存微信信息
    
    """

    params = {
        'msg_id': wxmessage_dict.get('msg_id'),
        'msg_timestamp': wxmessage_dict.get('msg_timestamp'),
        'msg_type': wxmessage_dict.get('msg_type'),
        'room_wxid': wxmessage_dict.get('room_wxid'),
        'wxid_from': wxmessage_dict.get('wxid_from'),
        'wxid_to': wxmessage_dict.get('wxid_to'),
        'atUserList': wxmessage_dict.get('atUserList'),
        'msg': wxmessage_dict.get('msg'),
        'raw_msg': wxmessage_dict.get('raw_msg'),
        'file_index': wxmessage_dict.get('file_index'),
        'file_name': wxmessage_dict.get('file_name'),
        'file_size': wxmessage_dict.get('file_size'),
        'emoji_url': wxmessage_dict.get('emoji_url'),
        'link_title': wxmessage_dict.get('link_title'),
        'link_desc': wxmessage_dict.get('link_desc'),
        'link_url': wxmessage_dict.get('link_url'),
        'link_img_url': wxmessage_dict.get('link_img_url'),
        'sub_type': wxmessage_dict.get('sub_type'),
        'user_id': wxmessage_dict.get('user_id'),
        'user_type': wxmessage_dict.get('user_type'),
        'create_at': wxmessage_dict.get('create_at'),
        'activity_id': wxmessage_dict.get('activity_id'),
    }
    mm_WxMessage.create(bot_wxid=bot_wxid, **params)

@shared_task
def update_wxgroup_name(room_wxid, new_name):
    """更新微信群名
    """
    mm_WxGroup.filter(room_wxid=room_wxid).update(name=new_name)
