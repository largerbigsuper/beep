#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('beep')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# app.conf.timezone = "Asia/Shanghai"
# app.conf.enable_utc = False

app.conf.beat_schedule = {
    'caculate-hotsearch-very-1-minute': {
        'task': 'beep.search.tasks.caculate_hotsearch',
        'schedule': crontab(minute='*'),
        'args': (),
    },
    # 每周一清除上周热搜
    'clear-hotsearch-very-monday': {
        'task': 'beep.search.tasks.clear_hotsearch',
        'schedule': crontab(day_of_week=1, hour=0, minute=0),
        'args': (),
    },
    'update-ticker-cache-every-30-seconds': {
        'task': 'beep.common.tasks.update_ticker_cache',
        'schedule': 30.0,
        'args': (),
    },
    'update-crawled-news-very-2-minute': {
        'task': 'beep.news.tasks.update_news_from_crawler',
        'schedule': crontab(minute='*/2'),
        'args': (),
    }
}


from kombu import Queue

app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default',    routing_key='task.#'),
    Queue('news', routing_key='news.#'),
)
task_default_exchange = 'tasks'
task_default_exchange_type = 'direct'
task_default_routing_key = 'task.default'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
