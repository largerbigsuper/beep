from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from beep.blog.models import Blog
from beep.activity.models import Activity

__all__ = ['bind_blog_to_activity']

@receiver(post_save, sender=Blog)
def bind_blog_to_activity(instance, raw, created, using, update_fields, **kwargs):
    """保存博文时更新活动相关博文信息
    """
    if instance.activity_id and instance.is_summary == True:
        instance.activity.summary_id = instance.id
        instance.activity.save()

@receiver(post_delete, sender=Blog)
def remove_blog_from_activity(instance, using, **kwargs):
    """删除博文时若是活动文章则设置活动文章为None
    """
    if instance.activity_id and instance.is_summary == True:
        instance.activity.summary_id = None
        instance.activity.save()