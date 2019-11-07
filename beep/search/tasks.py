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
    两天内带有话题的博文 阅读数 * 1 + 点赞数 * 1 + 评论数 * 1  + 搜索量
    1. 统计两天内的搜索历史单个记录词频
    2. 【新】话题产生时间小于2小时（前10）
    """
    search_days = 2
    limit = 100
    cornjob_logger.info('now: {}'.format(
        datetime.datetime.now().strftime(settings.DATETIME_FORMAT)))
    dt_end = datetime.datetime.now()
    dt_start = dt_end - timedelta(days=search_days)
    filter_range = (dt_start, dt_end)
    # 统计两天内的博文

    data_list = mm_user_Blog.filter(
        create_at__range=filter_range,
        topic_id__gt=0
    ).values(
        'topic_id',
        'topic__name',
        'topic__create_at'
    ).annotate(
        frequency=Sum('total_view') + Sum('total_comment') +
        Sum('total_like') + Sum('total_forward')
    ).order_by('-frequency')[:limit]
    data_list = list(data_list)
    topic_ids = [d['topic_id'] for d in data_list]
    # 转化为list
    data_search_list = mm_Topic.filter(pk__in=topic_ids).values('id', 'total_search', 'total_blog')
    search_dict = {}
    blog_dict = {}
    for d in data_search_list:
        search_dict[d['id']] = d['total_search']
        blog_dict[d['id']] = d['total_blog']

    for t in data_list:
        t['frequency'] += search_dict.get(t['topic_id'], 0)
        t['frequency'] += blog_dict.get(t['topic_id'], 0)
    
    sorted_data_list = sorted(data_list, key=lambda x: x['frequency'], reverse=True)
    
    # 处理【新】标签
    now = datetime.datetime.now()
    for d in sorted_data_list[:20]:
        if d['topic__create_at'].timestamp() + timedelta(hours=2).total_seconds() > now.timestamp():
            d['lable_type'] = 2

    hotsearch_list = []
    task = mm_SearchTask.new_task()
    for d in sorted_data_list:
        params = {
            'keyword': d['topic__name'],
            'frequency': d['frequency'],
            'lable_type': d.get('lable_type', 0),
            'create_at': dt_start,
            'update_at': dt_start,
            'task': task
        }
        item = HotSearch(**params)
        hotsearch_list.append(item)

    mm_HotSearch.bulk_create(hotsearch_list)
    
    task.status = 1
    task.end_at = datetime.datetime.now()
    task.save()
