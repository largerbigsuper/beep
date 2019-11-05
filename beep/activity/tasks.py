import time
import logging
import datetime

# from __future__ import absolute_import, unicode_literals
from celery import shared_task

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.conf import settings

logger = logging.getLogger('celery')


@shared_task
def send_rewardplan_start(rewardplan_id):
    """发送空投结果到直播频道

    1. 获取中奖名单
    2. 发送中奖消息到频道
    3. 更新rewardplan.task_result

    """
    msg_start = 'start send rewardplan message :<rewardplan_id: {}>'.format(
        rewardplan_id)
    msg_done = 'start send rewardplan message :<rewardplan_id: {}>'.format(
        rewardplan_id)
    logger.info(msg_start)
    # 1. 处理中奖名单
    from .models import mm_RewardPlan

    rewardplan = mm_RewardPlan.get(pk=rewardplan_id)
    # 生成中奖结果
    result_list = rewardplan.get_rewardplan_result
    rewardplan.task_result = 'successed'
    rewardplan.save()

    wx_groupwxid = rewardplan.activity.wx_groupwxid

    group_name = wx_groupwxid.replace('@chatroom', '')

    msg_dict = {
        'msg': '活动抽奖开始',
        'rewardplan': {
            'id': rewardplan.id,
            'desc': rewardplan.desc,
            'coin_name': rewardplan.coin_name,
            'coin_logo': rewardplan.coin_logo.url,
            'total_coin': rewardplan.total_coin,
            'start_time': rewardplan.start_time.strftime(settings.DATETIME_FORMAT)
        }
    }
    # 用户信息
    user = {
        'id': 0,
        'name': '系统消息',
        'avatar_url': '',
        'user_type': 'admin'
    }
    # 中奖信息
    data = {

    }
    message = {
        'msg_type': 'admin',
        'msg_dict': msg_dict,
        'user': user,
        'data': data
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name,
                                            {
                                                'type': 'chat_message',
                                                'message': message
                                            }
                                            )


    logger.info(msg_done)


