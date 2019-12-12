from celery import shared_task

from .models import mm_WxUser, mm_WxGroup, mm_WxBot

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
