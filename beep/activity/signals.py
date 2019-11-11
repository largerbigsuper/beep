from django.dispatch import receiver
from django.db.models.signals import pre_delete

from beep.blog.models import mm_Blog
from beep.activity.models import Activity

__all__ = ['delete_activity_blogs']

@receiver(pre_delete, sender=Activity)
def delete_activity_blogs(instance, using, **kwargs):
    """将活动绑定的文章设置为删除状态
    """
    mm_Blog.filter(activity_id=instance.id).update(is_delete=True)
