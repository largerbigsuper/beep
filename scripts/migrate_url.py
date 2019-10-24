# 更换域名

import json
from beep.activity.models import mm_Activity
from beep.blog.models import mm_Blog, mm_Topic
from beep.users.models import mm_User
from beep.news.models import mm_News

DOMAIN = 'http://pyc81u1xn.bkt.clouddn.com'
NEW_DOMAIN = 'http://imgbeepcrypto.lhxq.top'


def run():
    print('replace domain done')
    process_blog()
    process_activity()
    process_topic()
    process_news()
    process_user()
    print('replace domain done')

def process_blog():
    for obj in mm_Blog.all():
        obj.img_list = json.loads(json.dumps(obj.img_list).replace(DOMAIN, NEW_DOMAIN))
        obj.save()

def process_topic():
    for obj in mm_Topic.all():
        if not obj.cover:
            continue
        obj.cover = obj.cover.url.replace(DOMAIN, NEW_DOMAIN)
        obj.save()

def process_activity():
    for obj in mm_Activity.all():
        if not obj.cover:
            continue
        obj.cover = obj.cover.url.replace(DOMAIN, NEW_DOMAIN)
        obj.save()

def process_user():
    for obj in mm_User.all():
        obj.avatar_url = obj.avatar_url.replace(DOMAIN, NEW_DOMAIN)
        obj.save()

def process_news():
    for obj in mm_News.all():
        if not obj.post:
            continue
        obj.post = obj.post.url.replace(DOMAIN, NEW_DOMAIN)
        obj.save()

