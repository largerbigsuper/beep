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

    STATUS_CREATED = 0
    STATUS_PASSED = 1
    STATUS_REFUSED = 2
    STATUS_CHOICE = (
        (STATUS_CREATED, '正在审核'),
        (STATUS_PASSED, '审核通过'),
        (STATUS_REFUSED, '正在失败'),
    )

    def valid(self):
        return self.filter(status=self.STATUS_PASSED)

    def update_data(self, pk, field_name, amount=1):
        if amount > 0:
            value = F(field_name) + amount
        else:
            value = F(field_name) - abs(amount)
        updates = {
            field_name: value
        }
        self.filter(pk=pk).update(**updates)

    def recommand(self):
        end_at = datetime.datetime.now()
        return self.valid().filter(start_at__gte=end_at, is_recommand=True)


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
    coordinates = models.CharField(max_length=120, default='', blank=True, verbose_name='经度,纬度')
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
    summary_id = models.IntegerField(null=True, blank=True, verbose_name='总结博文id')
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
    is_recommand = models.BooleanField(default=False, blank=True, verbose_name='推荐')
    status = models.PositiveSmallIntegerField(choices=ActivityManager.STATUS_CHOICE,
                                              default=ActivityManager.STATUS_CREATED,
                                              verbose_name='审核状态')

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
    company = models.CharField(max_length=120, default='', blank=True, verbose_name='公司')
    address = models.CharField(max_length=120, default='', blank=True, verbose_name='地址')
    name = models.CharField(max_length=120, default='', blank=True, verbose_name='姓名')
    phone = models.CharField(max_length=120, default='', blank=True, verbose_name='手机号')

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
        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)
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
            selected_apply = choices(applys, k=self.total_luckyuser)
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




class ScheduleManager(ModelManager):
    
    def add_activity(self, user_id, activity, add_type='collect'):
        """添加活动
        """
        defaults = {
            'plan_datetime': activity.start_at
        } 
        if add_type == 'collect':
            defaults['is_collected'] = True
        elif add_type == 'registration':
            defaults['is_registrated'] = True
        self.update_or_create(user_id=user_id, activity_id=activity.id, defaults=defaults)


    def remove_activity(self, user_id, activity, add_type='collect'):
        """删除活动
        """
        obj = self.filter(user_id=user_id, activity_id=activity.id).first()
        if not obj:
            return
        if add_type == 'collect':
            obj.is_collected = False
        elif add_type == 'registration':
            obj.is_registrated = False
            
        if any([obj.is_registrated, obj.is_collected]):
            obj.save()
        else:
            obj.delete()

class Schedule(models.Model):
    """行程表
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='用户')
    plan_datetime = models.DateTimeField(verbose_name='计划时间')
    content = models.CharField(max_length=500, verbose_name='计划内容')
    activity = models.ForeignKey('activity.Activity', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='活动')
    is_registrated = models.BooleanField(default=False, verbose_name='活动报名')
    is_collected = models.BooleanField(default=False, verbose_name='活动收藏')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = ScheduleManager()

    class Meta:
        db_table = 'schedule'
        index_together = [
            ('user', 'plan_datetime')
        ]
        unique_together = [
            ['user', 'activity']
        ]
        ordering = ['-plan_datetime', '-id']


class WxFormManager(ModelManager):

    def valid(self):
        create_at = datetime.datetime.now() - timedelta(days=7)
        qs = self.filter(create_at__gt=create_at, published=False)
        return qs

    
    def add_form(self, user_id, activity_id, wxform_id):
        """添加记录
        """
        defaults = {
            'wxform_id': wxform_id
        }
        obj, created = self.update_or_create(user_id=user_id, activity_id=activity_id, defaults=defaults)
        return obj


class WxForm(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='用户')
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='活动')
    wxform_id = models.CharField(max_length=32, verbose_name='wxform_id')
    published = models.BooleanField(default=False, blank=True, verbose_name='已推送')
    create_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')

    objects = WxFormManager()

    class Meta:
        db_table = 'activity_wxform'
        unique_together = [
            ['user', 'activity']
        ]
        ordering = ['-id']
        verbose_name = '微信form'
        verbose_name_plural = '微信form'


mm_WxForm = WxForm.objects


mm_Schedule = Schedule.objects
mm_Activity = Activity.objects
mm_Registration = Registration.objects
mm_Collect = Collect.objects
mm_RewardPlan = RewardPlan.objects
mm_RewardPlanApply = RewardPlanApply.objects
