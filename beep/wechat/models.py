from django.conf import settings
from django.db import models
from django_extensions.db.fields.json import JSONField


from utils.modelmanager import ModelManager


class WxTemplateManager(ModelManager):
    
    WxFields_CN = {
        '新闻标题': 'thing2',
        '更新时间': 'date4',
        '温馨提示': 'thing5',
        '活动名称': 'thing1',
        '活动时间': 'data2'
    }
    WxFields_EN = {v: k for k, v in WxFields_CN.items()}

class WxTemplate(models.Model):

    name = models.CharField(max_length=100, verbose_name='模板名')
    code = models.CharField(max_length=64, verbose_name='模板id')
    tpl_id = models.PositiveIntegerField(default=0, verbose_name='模板编号')
    vars_list = JSONField(default='{}', blank=True, verbose_name='变量名列表')

    objects = WxTemplateManager()

    class Meta:
        db_table = 'wx_templates'
        ordering = ['-id']
        verbose_name = verbose_name_plural = '订阅消息模板'

    def __str__(self):
        return self.name


mm_WxTemplate = WxTemplate.objects


class WxSubscriptionManager(ModelManager):
    
    def add_subscription(self, user, code):
        wx_template = mm_WxTemplate.filter(code=code).first()
        if wx_template:
            obj, created = self.get_or_create(user=user, wx_template=wx_template)
            return obj

    def is_subscried(self, user, code):
        return self.filter(user=user, wx_template__code=code).exists()

class WxSubscription(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='用户')
    wx_template = models.ForeignKey(WxTemplate,
                                    on_delete=models.CASCADE,
                                    verbose_name='订阅消息模板')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = WxSubscriptionManager()

    class Meta:
        db_table = 'wx_subscriptions'
        ordering = ['-id']
        verbose_name = verbose_name_plural = '用户订阅'


mm_WxSubscription = WxSubscription.objects


class WxSubMessageManager(ModelManager):

    STATUS_DEFAULT = 0
    STATUS_SEND = 1
    STATUS_CHOICE = (
        (STATUS_DEFAULT, '未发送'),
        (STATUS_SEND, '已发送'),
    )

    hotsearch_dict = {
        'name': '资讯更新提醒',
        'code': '7r6MUUipAu9ZIdNIYeP2NuOJNQZVmML344JeldvPmvI',
        'tpl_id': 2142,
        'vars_list': {
            '新闻标题': 'thing2',
            '更新时间': 'date4',
            '温馨提示': 'thing5'
        }
    }

    activity_dict = {
        'name': '活动开始提醒',
        'code': 'eCbhJnmIktj4OsnBZkJdaYeSdpC3ZuwI5vOdl70io50',
        'tpl_id': 731,
        'vars_list': {
            '活动名称': 'thing1',
            '活动时间': 'date2'
        }
    }
    
    def send(self, pk):
        """发送活动开始通知
        """
        from .tasks import send_activity_start_notice
        send_activity_start_notice.delay(pk)


class WxSubMessage(models.Model):

    wx_template = models.ForeignKey(WxTemplate,
                                    on_delete=models.SET_NULL,
                                    null=True, verbose_name='模板消息')
    activity = models.ForeignKey('activity.Activity',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 db_constraint=False,
                                 verbose_name='活动')
    hotsearch = models.ForeignKey('search.HotSearch',
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             db_constraint=False,
                             verbose_name='热搜')
    title = models.CharField(max_length=20, default='', blank=True, verbose_name='热搜标题')
    warn_msg = models.CharField(max_length=20, default='Beep币扑不作为投资理财建议～', blank=True, verbose_name='温馨提示')
    status = models.PositiveSmallIntegerField(choices=WxSubMessageManager.STATUS_CHOICE,
                                              default=WxSubMessageManager.STATUS_DEFAULT,
                                              verbose_name='已发送')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = WxSubMessageManager()

    class Meta:
        db_table = 'wx_submessages'
        ordering = ['-id']
        verbose_name = verbose_name_plural = '推送订阅消息'


mm_WxSubMessage = WxSubMessage.objects
