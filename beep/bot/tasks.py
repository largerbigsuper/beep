import datetime
import random
from django.db.models import F
from django.db import transaction

from config.celery import app
from .models import mm_Bot, mm_BotActionStatsOnBlog, mm_BotComment, mm_BotActionLog
from beep.blog.models import Comment, mm_Comment, mm_Blog, mm_Like, mm_Point



"""
1.新增博文／文章／活动时，随机从语料库中摘选随机数字的评论
2.最少2条，随机评论8条封顶
3.每3条博文，安排1-2次转发，并引用语料库评论内容
4.每条博文，配随机数目的点赞（机器点赞18起步200封顶，均值保持在110上下，真实点赞可以继续叠加，不限制点赞数上限）
# 5.每场活动，随机机器人去提问（大佬厉害了！！有人跟我一样在币扑小程序围观吗？） 只发一次
6.新用户注册时，第一天，第二天，第五天及第七天，每天随机数目分配粉丝（每天2-6人之内）
"""

def get_bot():
    """
    1. 获取bot
    """
    return mm_Bot.get_bots().first()

def get_blog(bot_id=None, min_minutes=3, max_minutes=1200000, min_count=2, max_count=8, action='action_comment'):
    """
    2. 获取有效博文
        2.1 根据时间筛选符合条件的博文id
        2.2 根据bot执行记录剔除不符合的博文id
        2.3 随机筛选一个博文id

    Keyword Arguments:
        min_minutes {int} -- 最小发布时间 (default: {3})
        max_minutes {int} -- 最大发布时间 (default: {120})
        min_count {int} -- 最小机器评论数 (default: {2})
        max_count {int} -- 最大机器评论数 (default: {8})
    """
    # 根据时间筛选符合条件的博文id
    min_time = datetime.datetime.now() - datetime.timedelta(minutes=max_minutes)
    max_time = datetime.datetime.now() - datetime.timedelta(minutes=min_minutes)
    blogs = mm_Blog.filter(create_at__range=[min_time, max_time])
    blog_ids = {obj.id for obj in blogs}
    # 根据bot执行记录剔除不符合的博文id
    action_gt = action + '__gt'
    params = {
        'blog_id__in': blog_ids,
        action_gt: max_count
    }
    exclude_ids = mm_BotActionStatsOnBlog.filter(**params).values_list('blog_id', flat=True)
    params_log = {
        'blog_id__in': blog_ids,
        'bot_id': bot_id,
        'action': mm_BotActionLog.ACTION_MAP[action]
    }
    # 剔除已执行过的blog_id
    skip_ids = mm_BotActionLog.filter(**params_log).values_list('blog_id', flat=True)
    # 随机筛选一个博文id
    final_blogs = blog_ids - set(list(exclude_ids)) - set(list(skip_ids))
    if not final_blogs:
        return None
    else:
        return random.choice(list(final_blogs))

def get_comment(group=0):
    """
    获取单个评论
    """
    comment = mm_BotComment.get_random_one(group=group)
    if comment:
        text = comment.text
    else:
        text = '嗯，不错'
    return text

@app.task(queue='bot')
def task_add_blog_commnet():
    """
    单个bot执行评论单个博文
    博文增加评论
    """
    bot = get_bot()
    if not bot:
        return
    try:
        mm_Bot.run(bot.id)
        blog_id = get_blog()
        if not blog_id:
            return
        comment = get_comment()

        obj = _add_blog_comment(blog_id=blog_id, user_id=bot.user_id, commnet=comment)
        if obj:
            mm_BotActionStatsOnBlog.add_action(blog_id=blog_id, user_id=bot.user_id, action='action_comment')
            mm_BotActionLog.add_log(bot_id=bot.id, action='action_comment', rid=blog_id)
    finally:
        mm_Bot.stop(bot.id)


def _add_blog_comment(blog_id, user_id, commnet):
    """
    评论博文
    """
    blog = mm_Blog.get(pk=blog_id)
    to_user = blog.user
    instance = Comment(blog_id=blog_id, user_id=user_id,to_user=to_user, text=commnet)
    instance.save()
    blog.total_comment = F('total_comment') + 1
    blog.save()
    if blog.topic:
        blog.topic.total_comment = F('total_comment') + 1
        blog.topic.save()
    # 第一次评论
    mm_Comment.update_commnet_point(user_id=user_id)
    return instance


@app.task(queue='bot')
def task_add_blog_like():
    """
    博文点赞
    """
    bot = get_bot()
    if not bot:
        return
    try:
        mm_Bot.run(bot.id)
        blog_id = get_blog(min_count=2, max_count=200, action='action_like')
        if not blog_id:
            return

        obj = _add_blog_like(blog_id=blog_id, user_id=bot.user_id)
        if obj:
            mm_BotActionStatsOnBlog.add_action(blog_id=blog_id, user_id=bot.user_id, action='action_like')
            mm_BotActionLog.add_log(bot_id=bot.id, action='action_like', rid=blog_id)
    finally:
        mm_Bot.stop(bot.id)


def _add_blog_like(blog_id, user_id):
    """
    博文点赞
    """
    with transaction.atomic():
        obj, created = mm_Like.get_or_create(user_id=user_id, blog_id=blog_id)
        if created:
            mm_Blog.update_data(blog_id, 'total_like')
            mm_Point.add_action(user_id, mm_Point.ACTION_USER_ADD_BLOG_LIKE)
        return obj


@app.task(queue='bot')
def task_add_blog_forward():
    """
    博文转发
    1. 获取bot
    2. 获取有效博文
        2.1 根据时间筛选符合条件的博文id
        2.2 根据bot执行记录剔除不符合的博文id
        2.3 随机筛选一个博文id
    3. 获取一条博文评论
    4. 执行转发
    5. 记录bot执行记录
    """

    bot = get_bot()
    if not bot:
        return
    try:
        mm_Bot.run(bot.id)
        blog_id = get_blog(max_count=2, action='action_forward')
        if not blog_id:
            return
        text = get_comment()
        obj = _add_blog_forward(blog_id=blog_id, user_id=bot.user_id, text=text)
        if obj:
            mm_BotActionStatsOnBlog.add_action(blog_id=blog_id, user_id=bot.user_id, action='action_forward')
            mm_BotActionLog.add_log(bot_id=bot.id, action='action_forward', rid=blog_id)
    finally:
        mm_Bot.stop(bot.id)


def _add_blog_forward(blog_id, user_id, text):
    """
    执行转发
    """
    forward_blog = mm_Blog.get(pk=blog_id)
    params = {}
    if forward_blog.origin_blog_id:
        origin_blog_id = forward_blog.origin_blog_id
    else:
        origin_blog_id = forward_blog.id
    params['forward_blog_id'] = forward_blog.id
    params['origin_blog_id'] = origin_blog_id
    content = '@' + forward_blog.user.name + ' ' + text
    params['content'] = content
    params['user_id'] = user_id
    instance = mm_Blog.model(**params)
    instance.save()
    
    return instance


def task_add_user_following():
    """
    增加关注
    """
    pass


def task_add_activity_commnet():
    """
    博文增加评论
    """
    pass
