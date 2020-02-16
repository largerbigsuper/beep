import shortuuid
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import F

from .models import User, mm_User, mm_RelationShip, mm_Point

from beep.cfg.models import mm_AutoFollowingCfg

@receiver(post_save, sender=User)
def user_post_save(instance, raw, created, using, update_fields, **kwargs):
    """用户保存后操作
    """
    if created:
        add_auto_following(user=instance)
        add_invite_code(user=instance)
    
    complete_profile(user=instance)

def add_auto_following(user):
    """自动关注
    """
    followings = mm_AutoFollowingCfg.get_users()
    relations = []
    followings.append(user)
    for following in followings:
        relation = mm_RelationShip.model(user=user, following=following)
        relations.append(relation)
    objs = mm_RelationShip.bulk_create(relations)
    # 增加关注数
    mm_User.filter(pk=user.id).update(total_following= F('total_following') + len(objs))
    # 增加粉丝数
    for u in followings:
        mm_User.filter(pk=u.id).update(total_followers= F('total_followers') + 1)



def complete_profile(user):
    """完善用户信息赠送积分
    """
    if all([user.avatar_url, user.name, user.desc, user.account, user.openid]):
        if not user.completed_profile:
            mm_User.filter(pk=user.id).update(completed_profile=True)
            mm_Point.add_action(user_id=user.id, action=mm_Point.ACTION_USER_PROFILE)

def add_invite_code(user):
    """生成邀请码
    """
    invite_code = shortuuid.ShortUUID().random(length=6)
    mm_User.filter(pk=user.id).update(invite_code=invite_code)