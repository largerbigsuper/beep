import time
import logging
import datetime

# from __future__ import absolute_import, unicode_literals
from celery import shared_task

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger('celery')


@shared_task
def send_rewardplan_start(rewardplan_id):
    """发送空投结果到直播频道

    1. 获取中奖名单
    2. 发送中奖消息到频道
    3. 更新rewardplan.task_result

    """
    msg_start = 'start process rewardplan :<rewardplan_id: {}>'.format(
        rewardplan_id)
    msg_done = 'successed processed rewardplan :<rewardplan_id: {}>'.format(
        rewardplan_id)
    logger.info(msg_start)
    # 1. 处理中奖名单
    from .models import mm_RewardPlan

    # cache_key = 'task_{}'.format(rewardplan_id)
    # result = cache.get(cache_key)
    # if result:
    #     return

    rewardplan = mm_RewardPlan.get(pk=rewardplan_id)
    
    # 已经执行便跳过
    if rewardplan.task_result == 'successed':
        return

    # 频道为空跳过
    wx_groupwxid = rewardplan.activity.wx_groupwxid
    group_name = wx_groupwxid.replace('@chatroom', '')
    if not group_name:
        return

    # 生成中奖结果
    result_list = rewardplan.get_rewardplan_result
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
        'user_type': 2
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
    # 推送消息
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name,
                                            {
                                                'type': 'chat_message',
                                                'message': message
                                            }
                                            )
    # 更新结果
    mm_RewardPlan.filter(pk=rewardplan_id).update(task_result='successed')
    cache.set(cache_key, 'successed', 60 * 60)
    logger.info(msg_done)


