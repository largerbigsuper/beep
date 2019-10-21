from django.db import models
import datetime

from utils.modelmanager import ModelManager
from utils.post.gen_post import Post


class NewsManager(ModelManager):

    STATUS_EDITING = 0
    STATUS_PUBLISHED = 1
    STATUS_RECALL = 2

    STATUS_CHOICES = [
        (STATUS_EDITING, '编辑中'),
        (STATUS_PUBLISHED, '已发布'),
        (STATUS_RECALL, '已撤回')
    ]

    def published_news(self):
        return self.filter(status=self.STATUS_PUBLISHED)


class News(models.Model):
    """快讯
    """

    title = models.CharField(max_length=120, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    origin = models.CharField(max_length=40, blank=True, verbose_name='来源')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')
    status = models.PositiveSmallIntegerField(choices=NewsManager.STATUS_CHOICES,
                                              default=NewsManager.STATUS_EDITING, verbose_name='编辑状态')
    post = models.ImageField(blank=True, null=True, verbose_name='海报')

    objects = NewsManager()

    class Meta:
        db_table = 'news'
        verbose_name = verbose_name_plural = '快讯'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """保存快讯时生成海报
        """
        post_date = self.published_at if self.published_at else datetime.datetime.now()
        self.post = Post().generate_post(self.title, post_date, self.content)
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

mm_News = News.objects
