from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from beep.blog.models import (
    Blog, mm_Topic, mm_Blog,Blog_Blog, Blog_Article,
    mm_Topic,
    Comment)
from beep.activity.models import Activity, mm_Activity
from beep.users.models import mm_User

# FIXME
# post_save 使用时，其他接口注意保证调用save()的频率


@receiver(post_save, sender=Blog)
def post_save_blog(instance, raw, created, using, update_fields, **kwargs):
    """api调用"""
    _post_save_blog(instance, created)


@receiver(post_save, sender=Blog_Blog)
def post_save_blog_blog(instance, raw, created, using, update_fields, **kwargs):
    """后台调用"""
    _post_save_blog(instance, created)


@receiver(post_save, sender=Blog_Article)
def post_save_blog_article(instance, raw, created, using, update_fields, **kwargs):
    """后台调用"""
    _post_save_blog(instance, created)


def _post_save_blog(instance, created):
    """博文创建后勾子函数    
    """
    if created:
        # 博文总量
        mm_User.update_data(instance.user_id, 'total_blog')
        # 更新转发
        if instance.forward_blog_id:
            mm_Blog.update_data(instance.forward_blog_id, 'total_forward')
        # 更新话题
        if instance.topic_id:
            mm_Topic.update_data(instance.topic.id, 'total_blog')

    # 逻辑删除
    if instance.is_delete:
        post_delete_blog(instance)
    else:
        _post_save_blog_admin(instance, created)


def _post_save_blog_admin(instance, created):
    """后台更新文章关联到活动 
    """
    if instance.activity_id and instance.is_summary == True:
        # 不发送save信号
        mm_Activity.filter(pk=instance.activity_id).update(summary_id=instance.id)


def post_delete_blog(instance):
    """删除博文回调
    """
    # 更新活动绑定文章关系
    if instance.activity_id and instance.is_summary == True:
        mm_Activity.filter(pk=instance.activity_id).update(summary_id=None)
    # 更新我的博客个数
    mm_User.update_data(instance.user_id, 'total_blog', -1)
    # 跟新博文转发个数
    if instance.forward_blog_id:
        mm_Blog.update_data(instance.forward_blog_id, 'total_forward', -1)
    # 更新话题
    if instance.topic_id:
        mm_Topic.update_data(instance.topic.id, 'total_blog', -1)


# Comment
@receiver(post_delete, sender=Comment)
def post_delete_comment(instance, using, **kwargs):
    """删除评论
    """
    if instance.blog.topic_id:
        mm_Topic.update_data(instance.blog.topic_id, 'total_comment', -1)