from django.db import models
from django.db.models import F
from django.conf import settings

from django_extensions.db.fields.json import JSONField

from utils.modelmanager import ModelManager


class TopicManager(ModelManager):

    STATUS_BLOCKED = -1
    STATUS_NORMAL = 0
    STATUS_HOT = 1

    TOPIC_STATUS = (
        (STATUS_BLOCKED, '已屏蔽'),
        (STATUS_NORMAL, '正常话题'),
        (STATUS_HOT, '热门话题'),
    )

    TYPE_TOPIC = 0
    TYPE_ZhuanTiBang = 1
    TYPE_XinRenBang = 2

    TOPIC_TYPE = (
        (TYPE_TOPIC, '话题'),
        (TYPE_ZhuanTiBang, '专题榜'),
        (TYPE_XinRenBang, '新人榜')
    )

    def allowed_topics(self):
        return self.exclude(status=self.STATUS_BLOCKED)


class Topic(models.Model):
    """话题"""


    name = models.CharField(max_length=40, verbose_name='话题')
    status = models.PositiveSmallIntegerField(
        choices=TopicManager.TOPIC_STATUS,
        default=TopicManager.STATUS_NORMAL,
        verbose_name='状态屏蔽|正常|热门')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    total_view = models.PositiveIntegerField(default=0, verbose_name='查看人数')
    total_comment = models.PositiveIntegerField(default=0, verbose_name='评论次数')
    cover = models.ImageField(blank=True, null=True, verbose_name='封面图')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='topics',
                             blank=True,
                             null=True,
                             verbose_name='创建人')
    topic_type= models.PositiveSmallIntegerField(choices=TopicManager.TOPIC_TYPE, default=TopicManager.TYPE_TOPIC, verbose_name='话题|专题榜|新人榜')
    detail = models.TextField(blank=True, verbose_name='详情')

    objects = TopicManager()

    class Meta:
        db_table = 'topics'
        verbose_name = verbose_name_plural = '话题|专题|新人榜'

    def __str__(self):
        return '[{}]'.format(self.get_topic_type_display()) + self.name

class BlogManager(ModelManager):

    def my_blogs(self, user_id):
        return self.filter(user_id=user_id)

    def update_data(self, pk, field_name, amount=1):
        if amount > 0: 
            value = F(field_name) + amount
        else:
            value = F(field_name) - abs(amount)
        updates = {
            field_name: value
        }
        self.filter(pk=pk).update(**updates)


class Blog(models.Model):
    """博客"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='作者')
    topic = models.ForeignKey(Topic,
                              on_delete=models.DO_NOTHING,
                              related_name='blogs',
                              blank=True,
                              null=True,
                              verbose_name='话题')
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名')
    content = models.TextField(verbose_name='内容')
    img_list = JSONField(default='[]', verbose_name='图片列表')
    # [{"id": 1, "name": "9527"}, {"id": 2, "name": "9527"}]
    at_list = JSONField(default='[]', verbose_name='at用户列表')
    at_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      through='AtMessage',
                                      related_name='blog_at_users_set')
    shares = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    through='BlogShare',
                                    related_name='blog_shares_set')
    total_share = models.PositiveIntegerField(default=0, verbose_name='分享次数')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   through='Like',
                                   related_name='blog_likes_set')
    total_like = models.PositiveIntegerField(default=0, verbose_name='点赞次数')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      through='Comment',
                                      related_name='blog_comments_set',
                                      through_fields=('blog', 'user'))
    total_comment = models.PositiveIntegerField(default=0, verbose_name='评论次数')
    total_view = models.PositiveIntegerField(default=0, verbose_name='查看次数')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    forward_blog = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='forward_blogs', null=True, blank=True, verbose_name='转发blog_id')
    origin_blog = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='origin_blogs', null=True, blank=True, verbose_name='转发原始blog_id')
    total_forward = models.PositiveIntegerField(default=0, verbose_name='转发次数')
    video = models.CharField(max_length=200, blank=True, null=True, verbose_name='视频地址')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='文章标题')
    cover = models.CharField(max_length=200, blank=True, null=True, verbose_name='文章封面图')
    # activity = models.ForeignKey('activity.Activity', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='活动')


    objects = BlogManager()

    class Meta:
        db_table = 'blogs'
        ordering = ['-id']
        verbose_name = verbose_name_plural = '博文'


class LikeManager(ModelManager):
    
    def blogs(self):
        return self.filter(comment=None)

    def comments(self):
        return self.exculde(comment=None)


class Like(models.Model):
    """点赞记录
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='用户')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='博客')
    comment = models.ForeignKey('blog.Comment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='评论')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = LikeManager()

    class Meta:
        db_table = 'user_blog_like'
        unique_together = [
            ['user', 'blog', 'comment']
        ]
        ordering = ['-create_at']


class BlogShareManager(ModelManager):
    pass


class BlogShare(models.Model):
    """分享记录
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='用户')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='博客')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = BlogShareManager()

    class Meta:
        db_table = 'user_blog_share'
        unique_together = [
            ['user', 'blog']
        ]


class CommentManager(ModelManager):

    def valid(self):
        return self.filter(is_del=False)

    def my_commnets(self, user_id):
        return self.valid().filter(user_id=user_id)

    def update_data(self, pk, field_name, amount=1):
        if amount > 0: 
            value = F(field_name) + amount
        else:
            value = F(field_name) - abs(amount)
        updates = {
            field_name: value
        }
        self.filter(pk=pk).update(**updates)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, db_index=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_comments',
                             on_delete=models.CASCADE, db_index=False, verbose_name='评论人')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_replys',
                                on_delete=models.CASCADE, db_index=False, verbose_name='被回复的人')
    reply_to = models.ForeignKey('self', null=True, blank=True, related_name='reply_real',
                                 on_delete=models.DO_NOTHING, db_index=False, verbose_name='回复消息id')
    text = models.CharField(max_length=200, null=True,
                            blank=True, verbose_name='评论正文')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_del = models.BooleanField(default=False, verbose_name='删除')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='reply_group',
                                 on_delete=models.DO_NOTHING, db_index=False, verbose_name='回复消息的一级id')
    total_like = models.PositiveIntegerField(default=0, verbose_name='点赞数量')

    objects = CommentManager()

    class Meta:
        db_table = 'comments'
        index_together = [
            ('blog', 'user', 'reply_to', 'to_user')
        ]
        ordering = ['-create_at']
        verbose_name = '评论和回复管理'
        verbose_name_plural = '评论和回复管理'


class AtMessageManager(ModelManager):

    STATUS_CREATED = 0
    STATUS_READED = 1
    MESSAGE_STATUS = (
        (STATUS_CREATED, '未读'),
        (STATUS_CREATED, '已读'),
    )

    def my_messages(self, user_id, status=None):
        messages = self.filter(user_id=user_id)
        if status is not None:
            messages.filter(status=status)
        return messages


class AtMessage(models.Model):

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='博文')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='被@用户')
    status = models.PositiveSmallIntegerField(choices=AtMessageManager.MESSAGE_STATUS,
                                              default=AtMessageManager.STATUS_CREATED,
                                              verbose_name='未|已读')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = AtMessageManager()

    class Meta:
        db_table = 'at_messages'
        ordering = ['-create_at']


mm_Topic = Topic.objects
mm_Blog = Blog.objects
mm_Like = Like.objects
mm_BlogShare = BlogShare.objects
mm_Comment = Comment.objects
mm_AtMessage = AtMessage.objects
