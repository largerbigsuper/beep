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

