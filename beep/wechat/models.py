from django.conf import settings
from django.db import models
from django_extensions.db.fields.json import JSONField


from utils.modelmanager import ModelManager


class WxTemplateManager(ModelManager):
    
    WxFields_CN = {
        '新闻标题': 'thing2',
        '新闻摘要': 'thing3',
        '更新时间': 'date4',
        '温馨提示': 'thing5',
        '活动名称': 'thing1',
        '活动时间': 'data2'
    }
    WxFields_EN = {v: k for k, v in WxFields_CN.items()}

class WxTemplate(models.Model):

    name = models.CharField(max_length=100, verbose_name='模板名')
    code = models.CharField(max_length=64, verbose_name='模板id')
    vars_list = JSONField(default='[]', blank=True, verbose_name='变量名列表')

    objects = WxTemplateManager()

    class Meta:
        db_table = 'wx_templates'
        ordering = ['-id']
        verbose_name = verbose_name_plural = '订阅消息模板'


mm_WxTemplate = WxTemplate.objects


class WxSubscriptionManager(ModelManager):
    
    def add_subscription(self, user, code):
        wx_template = mm_WxTemplate.filter(code=code).first()
        if wx_template:
            obj, created = self.get_or_create(user=user, wx_template=wx_template)
            return obj


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


class WxSubMessage(models.Model):

    wx_template = models.ForeignKey(WxTemplate,
                                    on_delete=models.SET_NULL,
                                    null=True, verbose_name='模板消息')
    activity = models.ForeignKey('activity.Activity',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name='活动')
    news = models.ForeignKey('news.News',
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             verbose_name='快讯')
    status = models.PositiveSmallIntegerField(choices=WxSubMessageManager.STATUS_CHOICE,
                                              default=WxSubMessageManager.STATUS_DEFAULT,
                                              verbose_name='已发送')
    data = JSONField(default='{}', blank=True, verbose_name='post.body')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = WxSubMessageManager()

    class Meta:
        db_table = 'wx_submessages'
        ordering = ['-id']
        verbose_name = verbose_name_plural = '推送订阅消息'


mm_WxSubMessage = WxSubMessage.objects
