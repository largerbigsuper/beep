from django.db import models
from django.conf import settings

from utils.modelmanager import ModelManager
from django_extensions.db.fields.json import JSONField
from django.db.models import F


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

    def get_bots(self):
        return self.exclude(status=self.RUNING).filter(is_on=True)

    def run(self, pk):
        self.filter(pk=pk).update(status=self.RUNING)
    
    def stop(self, pk):
        self.filter(pk=pk).update(status=self.STOPED)

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

    def get_random_one(self, group=COMMENT_BLOG):
        return self.filter(group=group).order_by('?')[0]

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


class BotActionStatsManager(ModelManager):
    

    def add_action(self, rid, user_id, action):
        """
        增加action记录
        """
        if action in ['action_activity_comment']:
            obj, _ = self.get_or_create(activity_id=rid)
        else:
            obj, _ = self.get_or_create(blog_id=rid)
        updates = {}
        if action in ['action_comment', 'action_forward', 'action_like', 'action_activity_comment']:
            updates[action] = F(action) + 1
            self.filter(pk=obj.id).update(**updates)
        else:
            return

class BotActionStats(models.Model):
    """
    机器人对单个资源操作记录
    """
    blog = models.ForeignKey('blog.Blog', on_delete=models.CASCADE, null=True, blank=True, verbose_name='博文')
    activity = models.ForeignKey('activity.Activity', on_delete=models.CASCADE, null=True, blank=True, verbose_name='活动')
    action_activity_comment = models.IntegerField(default=0, verbose_name='活动评论次数')
    action_comment = models.IntegerField(default=0, verbose_name='评论次数')
    action_forward = models.IntegerField(default=0, verbose_name='转发次数')
    action_like = models.IntegerField(default=0, verbose_name='点赞次数')
    bots = JSONField(default=[], blank=True, verbose_name='机器人user_id')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    objects = BotActionStatsManager()

    class Meta:
        db_table = 'cms_bot_action_stats'
        verbose_name = '机器人操作Blog统计'
        verbose_name_plural = '机器人操作Blog统计'
        ordering = ['-id']

mm_BotActionStats = BotActionStats.objects


class BotActionLogManager(ModelManager):
    
    ACTION_BLOG_COMMNET = 0
    ACTION_BLOG_LIKE = 1
    ACTION_BLOG_FORWARD = 2
    ACTION_ACTIVITY_COMMENT = 3
    ACTION_USER_FOLLOWING = 4
    ACTION_CHOICES = (
        (ACTION_BLOG_COMMNET, '博文评论'),
        (ACTION_BLOG_LIKE, '博文点赞'),
        (ACTION_BLOG_FORWARD, '博文转发'),
        (ACTION_ACTIVITY_COMMENT, '活动评论'),
        (ACTION_USER_FOLLOWING, '关注用户'),
    )
    ACTION_BLOG = [ACTION_BLOG_COMMNET, ACTION_BLOG_LIKE, ACTION_BLOG_FORWARD]
    ACTION_ACTIVITY = [ACTION_ACTIVITY_COMMENT]
    ACTION_USER = [ACTION_USER_FOLLOWING]
    ACTION_ALL = [ACTION_BLOG_COMMNET, ACTION_BLOG_LIKE, ACTION_BLOG_FORWARD, ACTION_ACTIVITY_COMMENT, ACTION_USER_FOLLOWING]
    ACTION_MAP = {
        'action_comment': ACTION_BLOG_COMMNET,
        'action_like': ACTION_BLOG_LIKE,
        'action_forward': ACTION_BLOG_FORWARD,
        'action_activity_comment': ACTION_ACTIVITY_COMMENT,
        'action_user_following': ACTION_USER_FOLLOWING,
    }

    def add_log(self, bot_id, action, rid):
        """
        增加记录
        """
        action = self.ACTION_MAP.get(action)
        if action not in self.ACTION_ALL:
            return
        obj, _ = self.get_or_create(bot_id=bot_id, action=action, rid=rid)
        updates = {}
        updates['total'] = F('total') + 1
        self.filter(pk=obj.id).update(**updates)
    

class BotActionLog(models.Model):

    bot = models.ForeignKey('bot.Bot', on_delete=models.CASCADE, verbose_name='机器人')
    rid = models.PositiveIntegerField(default=0, verbose_name='资源id')
    action = models.PositiveSmallIntegerField(choices=BotActionLogManager.ACTION_CHOICES, default=BotActionLogManager.ACTION_BLOG_COMMNET, verbose_name='行为')
    total = models.PositiveIntegerField(default=0, verbose_name='次数')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = BotActionLogManager()

    class Meta:
        db_table = 'cms_bot_action_log'
        ordering = ['-id']
        verbose_name = '机器人操作日志'
        verbose_name_plural = '机器人操作日志'

mm_BotActionLog = BotActionLog.objects
