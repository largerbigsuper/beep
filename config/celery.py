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
    'update-ticker-cache-every-30-seconds': {
        'task': 'beep.common.tasks.update_ticker_cache',
        'schedule': 30.0,
        'args': (),
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
