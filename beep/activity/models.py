import logging
import datetime
from datetime import timedelta
from random import choices

from django.db import models
from django.db.models import F
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django_extensions.db.fields.json import JSONField

from beep.blog.models import mm_Blog
from config import celery_app
from utils.modelmanager import ModelManager
from .tasks import send_rewardplan_start

celery_logger = logging.getLogger('celery')

class ActivityManager(ModelManager):

    def update_data(self, pk, field_name, amount=1):
        if amount > 0:
            value = F(field_name) + amount
        else:
            value = F(field_name) - abs(amount)
        updates = {
            field_name: value
        }
        self.filter(pk=pk).update(**updates)


class Activity(models.Model):

    ON_LINE = 0
    OFF_LINE = 1
    ACTIVITY_TYPE_CHOICES = (
        (ON_LINE, '线上'),
        (OFF_LINE, '线下')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='发起人')
    title = models.CharField(max_length=120, verbose_name='标题')
    cover = models.ImageField(
        max_length=200, blank=True,
        null=True, verbose_name='封面图')
    activity_type = models.PositiveSmallIntegerField(
        choices=ACTIVITY_TYPE_CHOICES, default=ON_LINE, verbose_name='活动类型')
    start_at = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_at = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    ticket_price = models.FloatField(default=0, blank=True, verbose_name='费用（元）')
    province_code = models.CharField(
        max_length=40, null=True, blank=True, verbose_name='省code')
    province_name = models.CharField(
        max_length=40, null=True, blank=True, verbose_name='省')
    city_code = models.CharField(
        max_length=40, null=True, blank=True, verbose_name='市code')
    city_name = models.CharField(
        max_length=40, null=True, blank=True, verbose_name='市')
    district_code = models.CharField(
        max_length=40, null=True, blank=True, verbose_name='区code')
    district_name = models.CharField(
        max_length=40, null=True, blank=True, verbose_name='区')
    address = models.CharField(max_length=120, blank=True, verbose_name='具体位置信息')
    live_plateform = models.CharField(
        max_length=120, blank=True, verbose_name='直播平台')
    live_address = models.CharField(
        max_length=20, blank=True, verbose_name='直播地址|微信群名')
    total_user = models.PositiveIntegerField(default=0, blank=True, verbose_name='活动人数')
    contact_name = models.CharField(max_length=100, blank=True, verbose_name='联系人')
    contact_info = models.CharField(max_length=100, blank=True, verbose_name='联系人电话|微信')
    total_view = models.PositiveIntegerField(default=0, verbose_name='查看人数')
    total_registration = models.PositiveIntegerField(
        default=0, verbose_name='报名个数')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # content = models.TextField(blank=True, verbose_name='活动详情')
    content = RichTextUploadingField(blank=True, verbose_name='活动详情')
    total_collect = models.PositiveIntegerField(default=0, verbose_name='收藏数量')
    blog_id = models.IntegerField(null=True, blank=True, verbose_name='博文id')
    wx_groupname = models.CharField(
        max_length=200, blank=True, verbose_name='微信群名[后台获取]')
    wx_groupwxid = models.CharField(
        max_length=200, blank=True, verbose_name='微信群wxid[后台获取]')
    wx_botwxid = models.CharField(
        max_length=200, blank=True, verbose_name='微信机器人wxid[后台获取]')
    ask_allowed = models.BooleanField(default=False, verbose_name='是否可以提问')
    rewardplan = models.OneToOneField('activity.RewardPlan',
                                      on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      verbose_name='空投')

    objects = ActivityManager()

    class Meta:
        db_table = 'activity'
        ordering = ['-start_at']
        verbose_name = verbose_name_plural = '活动'

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """创建活动自动创建博文
        """
        if self.pk:
            return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        else:
            super().save(force_insert=force_insert, force_update=force_update,
                         using=using, update_fields=update_fields)
            params = {
                'user': self.user,
                'cover': self.cover,
                'title': '发布了活动：' + self.title,
                'activity': self
            }
            blog = mm_Blog.create(**params)
            self.blog_id = blog.id
            self.save()


class RegistrationManager(ModelManager):
    pass


class Registration(models.Model):
    """活动报名
    """

    STATUS_SUCCESS = 0
    REGISTRATION_STATUS_CHOICES = (
        (STATUS_SUCCESS, '成功'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='申请人')
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name='活动')
    status = models.PositiveSmallIntegerField(
        choices=REGISTRATION_STATUS_CHOICES, default=STATUS_SUCCESS)
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
        ordering = ['-create_at']
        verbose_name = verbose_name_plural = '活动报名'


class CollectManager(ModelManager):
    pass


class Collect(models.Model):
    """收藏记录
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='用户')
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name='博客')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = CollectManager()

    class Meta:
        db_table = 'activity_collect'
        unique_together = [
            ['user', 'activity']
        ]
        ordering = ['-create_at']


class RewardPlanManager(ModelManager):

    def update_task_status(self, rewardplan):
        # 更新空投计划后修改计划任务
        celery_logger.info('[celery] 更新空投<rewardplan: {}>'.format(rewardplan.id))
        # 已执行任务直接pass
        delta_time = rewardplan.start_time - datetime.datetime.now()
        if delta_time.seconds < 0:
            return
        
        # 取消之前任务
        if rewardplan.task_id:
            status = celery_app.AsyncResult(rewardplan.task_id).status
            result = celery_app.AsyncResult(rewardplan.task_id).result
            celery_logger.info('[celery] <task_id: {}, status: {}, result: {}>'.format(rewardplan.task_id, status, result))
            celery_logger.info('[celery] stop task_id: {}'.format(rewardplan.task_id))
            celery_app.control.revoke(rewardplan.task_id, terminate=True)

        # 新建任务

        eta = rewardplan.start_time - timedelta(microseconds=500)
        taskid = send_rewardplan_start.apply_async((rewardplan.id, ), eta=eta, ignore_result=False)
        rewardplan.task_id = taskid
        self.filter(pk=rewardplan.id).update(task_id=taskid)
        logger_msg = '[celery] new task_id'.format(taskid)
        celery_logger.info(logger_msg)


class RewardPlan(models.Model):
    """活动空投
    """
    desc = models.CharField(max_length=500, blank=True, verbose_name='描述')
    coin_name = models.CharField(max_length=100, verbose_name='代币名称')
    coin_logo = models.ImageField(verbose_name='代币logo')
    total_coin = models.IntegerField(default=0, verbose_name='代币数量')
    total_luckyuser = models.IntegerField(default=0, verbose_name='中奖人数')
    start_time = models.DateTimeField(verbose_name='开奖时间')
    applyers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      through='RewardPlanApply',
                                      through_fields=['rewardplan', 'user'],
                                      blank=True, )
    result = JSONField(default='[]', blank=True, verbose_name='中奖信息')
    task_id = models.CharField(max_length=120, db_index=True, null=True, blank=True, verbose_name='定时任务id')
    task_result = models.CharField(max_length=120,  null=True, blank=True, verbose_name='任务结果')

    objects = RewardPlanManager()

    class Meta:
        db_table = 'activity_reward'
        verbose_name = verbose_name_plural = '活动空投'
        ordering = ['-start_time']
    
    def __str__(self):
        return self.desc

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        # mm_RewardPlan.update_task_status(self)
        
    @property
    def get_rewardplan_result(self):
        """产生抽奖名单
        """
        if self.task_result:
            return self.result

        applys = list(mm_RewardPlanApply.filter(rewardplan=self).all())

        if self.total_luckyuser >= len(applys):
            selected_apply = applys
        else:
            selected_apply = choices(self.total_luckyuser, applys)
        result = []
        selected_pks = []
        for apply in selected_apply:
            u = {
                'id': apply.user.id,
                'name': apply.user.name,
                'avatar_url': apply.user.avatar_url_url,
                'address': apply.address
            }
            result.append(u)
            selected_pks.append(apply.id)
        self.result = result
        self.save()
        mm_RewardPlanApply.filter(pk__in=selected_pks).update(is_selected=True)
        
        return result

class RewardPlanApplyManager(ModelManager):
    pass


class RewardPlanApply(models.Model):
    """参加空投
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             db_constraint=False,
                             verbose_name='报名人')
    rewardplan = models.ForeignKey(RewardPlan,
                                   on_delete=models.SET_NULL,
                                   db_constraint=False,
                                   null=True,
                                   blank=True,
                                   verbose_name='空投')
    activity = models.ForeignKey(Activity,
                                 on_delete=models.SET_NULL,
                                 db_constraint=False,
                                 null=True,
                                 blank=True,
                                 verbose_name='活动')
    address = models.CharField(max_length=200, verbose_name='收币地址')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_selected = models.BooleanField(default=False, verbose_name='是否中奖')

    objects = RewardPlanApplyManager()

    class Meta:
        db_table = 'activity_reward_apply'
        unique_together = [
            ['user', 'rewardplan', 'activity']
        ]
        ordering = ['-activity', '-create_at']
        verbose_name = verbose_name_plural = '活动空投报名'

    def __str__(self):
        return '<{pk}: {user}>'.format(pk=self.id, user=self.user)


mm_Activity = Activity.objects
mm_Registration = Registration.objects
mm_Collect = Collect.objects
mm_RewardPlan = RewardPlan.objects
mm_RewardPlanApply = RewardPlanApply.objects
