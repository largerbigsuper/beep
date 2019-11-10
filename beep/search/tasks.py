import logging
import datetime
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.db.models import Sum, Count

from config.celery import app
from .models import HotSearch
from .models import mm_SearchTask, mm_SearchKeyWord, mm_SearchHistory, mm_HotSearch
from beep.blog.models import mm_Topic, mm_user_Blog


cornjob_logger = logging.getLogger('cornjob')


@app.task
def caculate_hotsearch():
    """生成热搜
    规则：
    两天内带有话题的博文 阅读数 * 1 + 点赞数 * 1 + 评论数 * 1  + 搜索量 + 博文数量 * 5
    1. 统计两天内的搜索历史单个记录词频
    2. 【新】话题产生时间小于2小时（前10）
    """
    cornjob_logger.info('task start..')
    search_days = 7
    limit = 100
    cornjob_logger.info('now: {}'.format(
        datetime.datetime.now().strftime(settings.DATETIME_FORMAT)))
    dt_end = datetime.datetime.now()
    dt_start = dt_end - timedelta(days=search_days)
    filter_range = (dt_start, dt_end)

    data_list = mm_user_Blog.filter(
        topic__topic_type=mm_Topic.TYPE_TOPIC,
        create_at__range=filter_range,
    ).values(
        'topic_id',
        'topic__name',
        'topic__create_at'
    ).annotate(
        frequency=Sum('total_view') + Sum('total_comment') + Sum('total_like') + Sum('total_forward') + 5 * Count('topic_id')
    ).order_by('-frequency')[:limit]

    print(str(data_list.query))
    data_list = list(data_list)
    topic_ids = [d['topic_id'] for d in data_list]
    
    sorted_data_list = sorted(data_list, key=lambda x: x['frequency'], reverse=True)
    
    # 处理【新】标签
    for d in sorted_data_list[:20]:
        if d['topic__create_at'] + timedelta(hours=2) > dt_end:
            d['lable_type'] = 2

    hotsearch_list = []
    task = mm_SearchTask.new_task()
    for d in sorted_data_list:
        params = {
            'keyword': d['topic__name'],
            'frequency': d['frequency'],
            'lable_type': d.get('lable_type', 0),
            'create_at': dt_end,
            'update_at': dt_end,
            'task': task
        }
        item = HotSearch(**params)
        hotsearch_list.append(item)

    mm_HotSearch.bulk_create(hotsearch_list)
    
    task.status = 1
    task.end_at = datetime.datetime.now()
    task.save()
