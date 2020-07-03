from django.db import models
from django.conf import settings

from utils.modelmanager import ModelManager
from django_extensions.db.fields.json import JSONField


class BotNameManager(ModelManager):
    pass


class BotName(models.Model):
    text = models.CharField(max_length=400, verbose_name='内容')
    used = models.BooleanField(default=False, verbose_name='已使用')
    
    objects = BotNameManager()

    class Meta:
        db_table = 'cms_bot_name'
        verbose_name = '机器人名子'
        verbose_name_plural = '机器人名子'
        ordering = ['-id']

mm_BotName = BotName.objects


class BotNameBuilderManager(ModelManager):
    pass


class BotNameBuilder(models.Model):

    text = models.TextField(verbose_name='输入导入数据【以换行符区分】')
    done = models.BooleanField(default=False, verbose_name='执行成功')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = BotNameBuilderManager()

    class Meta:
        db_table = 'cms_bot_name_builder'
        verbose_name = '生成机器人姓名批量生成'
        verbose_name_plural = '生成机器人姓名批量生成'
        ordering = ['-id']


mm_BotNameBuilder = BotNameBuilder.objects


class BotAvatarManager(ModelManager):
    pass


class BotAvatar(models.Model):
    text = models.CharField(max_length=400, verbose_name='内容')
    used = models.BooleanField(default=False, verbose_name='已使用')
    
    objects = BotAvatarManager()

    class Meta:
        db_table = 'cms_bot_avatar'
        verbose_name = '机器人头像'
        verbose_name_plural = '机器人头像'
        ordering = ['-id']

mm_BotAvatar = BotAvatar.objects


class BotAvatarBuilderManager(ModelManager):
    pass


class BotAvatarBuilder(models.Model):

    text = models.TextField(verbose_name='输入导入数据【以换行符区分】')
    done = models.BooleanField(default=False, verbose_name='执行成功')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = BotAvatarBuilderManager()

    class Meta:
        db_table = 'cms_bot_avatar_builder'
        verbose_name = '生成机器人头像批量生成'
        verbose_name_plural = '生成机器人头像批量生成'
        ordering = ['-id']


mm_BotAvatarBuilder = BotAvatarBuilder.objects


class BotBuilderManager(ModelManager):
    pass


class BotBuilder(models.Model):

    desc = models.CharField(max_length=100, verbose_name='描述')
    total = models.PositiveIntegerField(default=1, verbose_name='生成机器人个数')
    done = models.BooleanField(default=False, verbose_name='执行成功')
    results = JSONField(default=[], blank=True, verbose_name='机器人列表')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = BotBuilderManager()

    class Meta:
        db_table = 'cms_bot_builder'
        verbose_name = '生成机器人生成'
        verbose_name_plural = '生成机器人生成'
        ordering = ['-id']


mm_BotBuilder = BotBuilder.objects


class BotManager(ModelManager):
    
    STOPED = 0
    RUNING = 1
    
    STATUS_CHOICES = (
        (STOPED, '停止'),
        (RUNING, '运行中'),
    )


class Bot(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    status = models.PositiveSmallIntegerField(choices=BotManager.STATUS_CHOICES, default=BotManager.STOPED, verbose_name='运行状态')
    is_on = models.BooleanField(default=True, verbose_name='使用中')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    objects = BotManager()

    class Meta:
        db_table = 'cms_bot'
        verbose_name = '机器人'
        verbose_name_plural = '机器人'
        ordering = ['-id']

mm_Bot = Bot.objects


class BotCommentManager(ModelManager):

    COMMENT_BLOG = 0
    COMMENT_ACTIVITY = 1
    GROUP_CHOICES = (
        (COMMENT_BLOG, '博文评论'),
        (COMMENT_ACTIVITY, '活动评论'),
    )


class BotComment(models.Model):

    group = models.PositiveSmallIntegerField(choices=BotCommentManager.GROUP_CHOICES, default=BotCommentManager.COMMENT_BLOG)
    text = models.CharField(max_length=200, verbose_name='语句库')

    objects = BotCommentManager()

    class Meta:
        db_table = 'cms_bot_commnet'
        verbose_name = '评论库'
        verbose_name_plural = '评论库'
        ordering = ['-id']

mm_BotComment = BotComment.objects

