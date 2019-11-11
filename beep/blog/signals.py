from django.dispatch import receiver
from django.db.models.signals import post_save

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

