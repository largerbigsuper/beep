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
    mm_WxMessage.create(bot_wxid=bot_wxid, **wxmessage_dict)

@shared_task
def update_wxgroup_name(room_wxid, new_name):
    """更新微信群名
    """
    mm_WxGroup.filter(room_wxid=room_wxid).update(name=new_name)
