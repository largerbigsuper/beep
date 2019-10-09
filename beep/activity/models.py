from django.db import models
from django.conf import settings

from utils.modelmanager import ModelManager

class ActivityManager(ModelManager):
    pass


class Activity(models.Model):

    ON_LINE = 0
    OFF_LINE = 1
    ACTIVITY_TYPE_CHOICES = (
        (ON_LINE, '线上'),
        (OFF_LINE, '线下')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='发起人')
    title = models.CharField(max_length=120, verbose_name='标题')
    cover = models.CharField(max_length=200, verbose_name='封面图')
    activity_type = models.PositiveSmallIntegerField(choices=ACTIVITY_TYPE_CHOICES, default=ON_LINE, verbose_name='活动类型')
    start_at = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_at = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    ticket_price = models.FloatField(default=0, verbose_name='费用（元）')
    area = models.ForeignKey('common.Area', on_delete=models.DO_NOTHING, verbose_name='区域')
    address = models.CharField(max_length=120, verbose_name='具体位置信息')
    live_plateform = models.CharField(max_length=120, blank=True, verbose_name='直播平台')
    live_address = models.CharField(max_length=20, blank=True, verbose_name='直播地址|微信群名')
    total_user = models.PositiveIntegerField(default=0, verbose_name='活动人数')
    contact_name = models.CharField(max_length=100, verbose_name='联系人')
    contact_info = models.CharField(max_length=100, verbose_name='联系人电话|微信')
    total_view = models.PositiveIntegerField(default=0, verbose_name='查看人数')
    total_registration = models.PositiveIntegerField(default=0, verbose_name='报名个数')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    content = models.TextField(blank=True, verbose_name='活动详情')
    
    
    objects = ActivityManager()

    class Meta:
        db_table = 'activity'
        ordering = ['-id']


class RegistrationManager(ModelManager):
    pass


class Registration(models.Model):
    """活动报名
    """

    STATUS_SUCCESS = 0
    REGISTRATION_STATUS_CHOICES = (
        (STATUS_SUCCESS, '成功'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='申请人')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='活动')
    status = models.PositiveSmallIntegerField(choices=REGISTRATION_STATUS_CHOICES, default=STATUS_SUCCESS)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')

    objects = RegistrationManager()

    class Meta:
        db_table = 'registration'
        index_together = [
            ['user', 'activity'],
            ]
        unique_together = [
            ['user', 'activity'],
            ]

mm_Activity = Activity.objects
mm_Registration = Registration.objects
