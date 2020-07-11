import datetime
import random
from django.db.models import F, Count
from django.db import transaction

from config.celery import app
from .models import mm_Bot, mm_BotActionStats, mm_BotComment, mm_BotActionLog, mm_BotTask
from beep.blog.models import Comment, mm_Comment, mm_Blog, mm_Like, mm_Point
from beep.activity.models import mm_Activity
from beep.users.models import mm_User, mm_RelationShip



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

def get_activity(bot_id=None, min_minutes=3, max_minutes=1200000, min_count=0, max_count=1, action='action_activity_comment'):
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
    qs = mm_Activity.filter(create_at__range=[min_time, max_time])
    obj_ids = {obj.id for obj in qs}
    # 根据bot执行记录剔除不符合的博文id
    action_gt = action + '__gt'
    params = {
        'activity_id__in' : obj_ids,
        action_gt: max_count
    }
    obj_count_limit_ids = mm_BotActionStats.filter(**params).values_list('activity_id', flat=True)
    params_log = {
        'rid__in': obj_ids,
        'bot_id': bot_id,
        'action': mm_BotActionLog.ACTION_MAP[action]
    }
    # 剔除已执行过的blog_id
    obj_bot_limit_ids = mm_BotActionLog.filter(**params_log).values_list('rid', flat=True)
    # 随机筛选一个博文id
    final_ids = obj_ids - set(list(obj_count_limit_ids)) - set(list(obj_bot_limit_ids))
    if not final_ids:
        return None
    else:
        return random.choice(list(final_ids))

def get_blog(bot_id=None, min_minutes=3, max_minutes=7200, min_count=2, max_count=8, action='action_comment'):
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
    obj_ids = {obj.id for obj in blogs}
    # 根据bot执行记录剔除不符合的博文id
    action_gt = action + '__gt'
    params = {
        'blog_id__in': obj_ids,
        action_gt: max_count
    }
    obj_count_limit_ids = mm_BotActionStats.filter(**params).values_list('blog_id', flat=True)
    params_log = {
        'rid__in': obj_ids,
        'bot_id': bot_id,
        'action': mm_BotActionLog.ACTION_MAP[action]
    }
    # 剔除已执行过的blog_id
    obj_bot_limit_ids = mm_BotActionLog.filter(**params_log).values_list('rid', flat=True)
    # 随机筛选一个博文id
    final_blogs = obj_ids - set(list(obj_count_limit_ids)) - set(list(obj_bot_limit_ids))
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
def task_add_blog_comment():
    """
    单个bot执行评论单个博文
    博文增加评论
    """
    mm_BotTask.task_keep_open('task_add_blog_comment')
    bot = get_bot()
    if not bot:
        return
    try:
        mm_Bot.run(bot.id)
        blog_id = get_blog(bot_id=bot.id)
        if not blog_id:
            return
        comment = get_comment()

        obj = _add_blog_comment(blog_id=blog_id, user_id=bot.user_id, commnet=comment)
        if obj:
            mm_BotActionStats.add_action(rid=blog_id, user_id=bot.user_id, action='action_comment')
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
    mm_BotTask.task_keep_open('task_add_blog_like')
    bot = get_bot()
    if not bot:
        return
    try:
        mm_Bot.run(bot.id)
        blog_id = get_blog(bot_id=bot.id, min_count=2, max_count=200, action='action_like')
        if not blog_id:
            return

        obj = _add_blog_like(blog_id=blog_id, user_id=bot.user_id)
        if obj:
            mm_BotActionStats.add_action(rid=blog_id, user_id=bot.user_id, action='action_like')
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
    mm_BotTask.task_keep_open('task_add_blog_forward')
    bot = get_bot()
    if not bot:
        return
    try:
        mm_Bot.run(bot.id)
        blog_id = get_blog(bot_id=bot.id, max_count=2, action='action_forward')
        if not blog_id:
            return
        text = get_comment()
        obj = _add_blog_forward(blog_id=blog_id, user_id=bot.user_id, text=text)
        if obj:
            mm_BotActionStats.add_action(rid=blog_id, user_id=bot.user_id, action='action_forward')
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

@app.task(queue='bot')
def task_add_activity_commnet():
    """
    活动增加评论
    """
    mm_BotTask.task_keep_open('task_add_activity_commnet')
    bot = get_bot()
    if not bot:
        return
    try:
        mm_Bot.run(bot.id)
        rid = get_activity(bot_id=bot.id, max_count=1, action='action_activity_comment')
        if not rid:
            return
        text = get_comment()
        obj = _add_activity_comment(rid=rid, user_id=bot.user_id, text=text)
        if obj:
            mm_BotActionStats.add_action(rid=rid, user_id=bot.user_id, action='action_activity_comment')
            mm_BotActionLog.add_log(bot_id=bot.id, action='action_activity_comment', rid=rid)
    finally:
        mm_Bot.stop(bot.id)


def _add_activity_comment(rid, user_id, text):
    """
    活动评论
    """
    blog = mm_Blog.get(activity_id=rid)
    to_user = blog.user
    instance = Comment(blog_id=blog.id, user_id=user_id,to_user=to_user, text=text)
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
def task_add_user_following(signup_day=1):
    """
    每天固定时间跑三次
    增加关注
    6.新用户注册时，第一天，第二天，第五天及第七天，每天随机数目分配粉丝（每天2-6人之内）
        6.1 每个机器人关注个数小于200
        6.2 一个机器人一天只跑一次任务
        6.3 单次最多关注10人
        6.4 单个普通账户一天增加粉丝 2～6人
    """
    mm_BotTask.task_keep_open('task_add_user_following')

    bot = get_bot()
    if not bot:
        return
    try:
        mm_Bot.run(bot.id)
        rids = get_users_not_following(signup_day=signup_day, user_id=bot.user.id, max_users=10, max_bot_per_day=6)
        for rid in rids:
            _add_user_following(user_id=bot.user.id, following_id=rid)
            mm_BotActionLog.add_log(bot_id=bot.id, action='action_user_following', rid=rid)
    finally:
        mm_Bot.stop(bot.id)

def get_users_not_following(signup_day, user_id, max_users=10, max_bot_per_day=6):
    """
    获取符合要求的用户

    Keyword Arguments:
        signup_day {int} -- 注册第几天 (default: {signup_day})
        bot_id {int} -- bot_id (default: {bot.id})
        max_users {int} -- 最多关注几人 (default: {10})
        max_bot_per_day {int} -- 单个用户每天机器粉限制 (default: {6})
    """
    # create_at
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=signup_day-1)
    user_filters = {
        'create_at__date': start_date,
        'is_bot': False,
    }
    user_ids = mm_User.filter(**user_filters).values_list('id', flat=True)
    if not user_ids:
        return []
    # 去除已关注
    relation_filters = {
        'user_id': user_id
    }
    following_ids = set(list(mm_RelationShip.filter(**relation_filters).values_list('following_id', flat=True)))
    not_following_ids = [uid for uid in user_ids if uid not in following_ids]
    if not not_following_ids:
        return []
    # 每天关注人数限制
    today_date = datetime.date.today()
    following_limit_filter = {
        'following_id__in': not_following_ids,
        'user__is_bot': True,
        'create_at__date': today_date
    }
    out_limited_ids = mm_RelationShip.filter(**following_limit_filter).values('following_id').annotate(total_following=Count('user')).filter(total_following__gt=max_bot_per_day).values_list('following_id', flat=True)

    expected_ids = [uid for uid in not_following_ids if uid not in out_limited_ids]

    return expected_ids[:max_users]


def _add_user_following(user_id, following_id):
    """
    添加关注
    """
    relation = mm_RelationShip.add_relation(user_id=user_id, following_id=following_id)
    # 更新统计
    # 更新我的关注个数
    mm_User.update_data(user_id, 'total_following')
    # 更新我的粉丝个数
    mm_User.update_data(following_id, 'total_followers')
    return relation


@app.task(queue="bot")
def task_add_user_following_after_create_blog():
    """
    创建博文后两天随机增加关注
    用户每新发一条博文／文章／活动，两天内，随机增加3-8个粉丝
    """
    mm_BotTask.task_keep_open('task_add_user_following_after_create_blog')
    # 筛选符合的blog
    date_before = datetime.date.today() - datetime.timedelta(days=2)
    blog_filter = {
        "create_at__date__gt": date_before
    }
    blogs = mm_Blog.filter(**blog_filter).values_list('id', "user_id")
    blog_dict = dict(list(blogs))
    # 筛选剔除已满足的blog
    log_filter = {
        "action": mm_BotActionLog.ACTION_BLOG_ADD_FOLLOWING,
        "total__gt": 8
    }
    done_blog_ids = list(mm_BotActionLog.filter(**log_filter).values_list('rid', flat=True))
    usable_blog_ids = [blog_id for blog_id in blog_dict.keys() if blog_id not in done_blog_ids]
    if not usable_blog_ids:
        return
    # 随机选择一个blog_id
    rid = random.choice(usable_blog_ids)
    following_id = blog_dict[rid]
    # rid = 18159
    # following_id = 24
    # 剔除已关注的bot
    following_bot_uids = mm_RelationShip.filter(following_id=following_id, user__is_bot=True).values_list('user_id', flat=True)
    bot = mm_Bot.exclude(user_id__in=following_bot_uids).order_by("?").first()
    if bot:
        _add_user_following(user_id=bot.user_id, following_id=following_id)
        mm_BotActionLog.add_log(bot_id=bot.id, action=mm_BotActionLog.ACTION_BLOG_ADD_FOLLOWING, rid=rid)