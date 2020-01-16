from django.db import models
from django.conf import settings

from utils.modelmanager import ModelManager

class AutoFollowingCfgManager(ModelManager):
    
    def get_users(self):
        queryset = self.all().select_related('user')
        users = [obj.user for obj in queryset]
        return users


class AutoFollowingCfg(models.Model):
    """用户自动关注表
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    
    objects = AutoFollowingCfgManager()

    class Meta:
        db_table = 'beep_auto_following_cfg'
        ordering = ['-id']
        
        verbose_name = '用户自动关注配置'
        verbose_name_plural = '用户自动关注配置'


mm_AutoFollowingCfg = AutoFollowingCfg.objects


class ActionPointCfgManager(ModelManager):
    
    def get_action_point_mapping(self):
        cfg_list = list(self.all().values_list('code', 'point'))
        return dict(cfg_list)

class ActionPointCfg(models.Model):
    """用户行为积分奖励设置
    """
    code = models.PositiveIntegerField(default=0, unique=True, verbose_name='编号')
    name = models.CharField(max_length=100, verbose_name='行为')
    point = models.PositiveIntegerField(default=0, verbose_name='奖励积分')
    is_on = models.BooleanField(default=True, verbose_name='应用中')

    objects = ActionPointCfgManager()

    class Meta:
        db_table = 'beep_action_point_cfg'
        ordering = ['code']
        verbose_name = '用户行为积分配置'
        verbose_name_plural = '用户行为积分配置'

mm_ActionPointCfg = ActionPointCfg.objects
