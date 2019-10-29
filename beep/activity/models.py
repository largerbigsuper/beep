from django.db import models
from django.db.models import F
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from beep.blog.models import mm_Blog
from utils.modelmanager import ModelManager

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='发起人')
    title = models.CharField(max_length=120, verbose_name='标题')
    cover = models.ImageField(max_length=200, blank=True, null=True, verbose_name='封面图')
    activity_type = models.PositiveSmallIntegerField(choices=ACTIVITY_TYPE_CHOICES, default=ON_LINE, verbose_name='活动类型')
    start_at = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_at = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    ticket_price = models.FloatField(default=0, verbose_name='费用（元）')
    province_code = models.CharField(max_length=40, null=True, blank=True, verbose_name='省code')
    province_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='省')
    city_code = models.CharField(max_length=40, null=True, blank=True, verbose_name='市code')
    city_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='市')
    district_code = models.CharField(max_length=40, null=True, blank=True, verbose_name='区code')
    district_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='区')
    address = models.CharField(max_length=120, verbose_name='具体位置信息')
    live_plateform = models.CharField(max_length=120, blank=True, verbose_name='直播平台')
    live_address = models.CharField(max_length=20, blank=True, verbose_name='直播地址|微信群名')
    total_user = models.PositiveIntegerField(default=0, verbose_name='活动人数')
    contact_name = models.CharField(max_length=100, verbose_name='联系人')
    contact_info = models.CharField(max_length=100, verbose_name='联系人电话|微信')
    total_view = models.PositiveIntegerField(default=0, verbose_name='查看人数')
    total_registration = models.PositiveIntegerField(default=0, verbose_name='报名个数')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # content = models.TextField(blank=True, verbose_name='活动详情')
    content = RichTextUploadingField(blank=True, verbose_name='活动详情')
    total_collect = models.PositiveIntegerField(default=0, verbose_name='收藏数量')
    blog_id = models.IntegerField(null=True, blank=True, verbose_name='博文id')
    wx_groupname = models.CharField(max_length=200, blank=True, verbose_name='微信群名[后台获取]')
    wx_groupwxid = models.CharField(max_length=200, blank=True, verbose_name='微信群wxid[后台获取]')
    wx_botwxid = models.CharField(max_length=200, blank=True, verbose_name='微信机器人wxid[后台获取]')
    
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
            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
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
        ordering = ['-create_at']
        verbose_name = verbose_name_plural = '活动报名'


class CollectManager(ModelManager):
    pass


class Collect(models.Model):
    """收藏记录
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='用户')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='博客')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = CollectManager()

    class Meta:
        db_table = 'activity_collect'
        unique_together = [
            ['user', 'activity']
        ]
        ordering = ['-create_at']


mm_Activity = Activity.objects
mm_Registration = Registration.objects
mm_Collect = Collect.objects
