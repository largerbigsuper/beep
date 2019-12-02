import datetime
from random import choice

from django.db import models
from django.db.models import Subquery

from beep.users.models import mm_RelationShip
from utils.modelmanager import ModelManager


class AdManager(ModelManager):

    TYPE_BOLG_FOLLOWING = 0
    TYPE_BLOG_HOT = 1
    TYPE_TOPIC_HOT = 2
    TYPE_LINK = 3

    AD_TYPE = (
        (TYPE_BOLG_FOLLOWING, '博文关注'),
        (TYPE_BLOG_HOT, '博文热门'),
        (TYPE_TOPIC_HOT, '热搜榜'),
        (TYPE_LINK, '图文链接'),
    )

    MODULE_NONE = 0
    MODULE_HOME = 1
    MODULE_HOT_SEARCH_LIST = 2
    MODULE_NEWS_LIST = 3
    MODULE_BLOG_DETAIL = 4
    MODULE_TOPIC_DETAIL = 5
    MODULE_ACTIVITY_DETAIL = 6
    MODULE_HOT_SEARCH_DETAIL = 7
    MODULE_NEWS_DETAIL = 8

    MODULE_TYPE = (
        (MODULE_NONE, '未设置'),
        (MODULE_HOME, '首页'),
        (MODULE_HOT_SEARCH_LIST, '热搜'),
        (MODULE_NEWS_LIST, '快讯'),
        (MODULE_BLOG_DETAIL, '博文详情'),
        (MODULE_TOPIC_DETAIL, '专题详情'),
        (MODULE_ACTIVITY_DETAIL, '活动详情'),
        (MODULE_HOT_SEARCH_DETAIL, '热搜详情'),
        (MODULE_NEWS_DETAIL, '快讯详情'),
    )

    POSITION_NONE = 0
    POSITION_MAIN = 1
    POSITION_SIDE = 2

    POSITION_TYPE = (
        (POSITION_NONE, '未设置'),
        (POSITION_MAIN, '主位置'),
        (POSITION_SIDE, '侧边栏'),
    )

    STAUTS_EDITING = 0
    STATUS_PUBLISHED = 1
    STATUS_REVOKE = 2
    STATUS_TYPE = (
        (STAUTS_EDITING, '编辑中'),
        (STATUS_PUBLISHED, '已发布'),
        (STATUS_REVOKE, '已撤回'),
    )

    def valid(self):
        now = datetime.datetime.now()
        return self.filter(status=self.STATUS_PUBLISHED, expired_at__gt=now, start_at__lt=now)

    def get_blog_following_ad(self, user_id):
        """获取关注推荐广告
        """
        following_users = mm_RelationShip.filter(user_id=user_id).values_list('following_id', flat=True)
        ad_list = list(self.valid().filter(ad_type=self.TYPE_BOLG_FOLLOWING, blog__user_id__in=Subquery(following_users)).select_related('blog'))
        if ad_list:
            obj = choice(ad_list)
            return obj.blog
        else:
            return None

    def get_blog_hot_ad(self):
        """获取热门博文广告
        """
        ad_list = list(self.valid().filter(ad_type=self.TYPE_BLOG_HOT).select_related('blog'))
        ad_blog_dict = {}
        for ad in ad_list:
            ad_blog_dict[ad.order_num] = ad.blog
        return ad_blog_dict


    def get_hot_search_ad(self):
        """获取热搜广告
        """
        ad_list = list(self.valid().filter(ad_type=self.TYPE_TOPIC_HOT).select_related('hotSearch'))
        ad_hotSearch_dict = {}
        for ad in ad_list:
            ad_hotSearch_dict[ad.order_num] = ad.hotSearch
        return ad_hotSearch_dict



class Ad(models.Model):
    """博文相关广告
    """
    ad_type = models.PositiveSmallIntegerField(
        choices=AdManager.AD_TYPE,
        default=AdManager.TYPE_LINK,
        verbose_name='广告类型')
    blog = models.ForeignKey('blog.Blog',
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             verbose_name='博文')
    hotSearch = models.ForeignKey('search.HotSearch',
                              on_delete=models.SET_NULL,
                              null=True, blank=True,
                              verbose_name='热搜')
    order_num = models.PositiveIntegerField(default=1, verbose_name='排列位置')
    image = models.ImageField(blank=True, null=True, verbose_name='广告封面')
    link = models.CharField(max_length=200, default='', blank=True, verbose_name='广告链接')
    module_type = models.PositiveSmallIntegerField(choices=AdManager.MODULE_TYPE,
                                                   default=AdManager.TYPE_BOLG_FOLLOWING,
                                                   db_index=True,
                                                   verbose_name='显示模块'
                                                   )
    position_type = models.PositiveSmallIntegerField(choices=AdManager.POSITION_TYPE,
                                                     default=AdManager.POSITION_NONE,
                                                     db_index=True,
                                                     verbose_name='显示位置'
                                                     )
    start_at = models.DateTimeField(verbose_name='生效时间')
    expired_at = models.DateTimeField(verbose_name='结束时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.PositiveSmallIntegerField(choices=AdManager.STATUS_TYPE,
                                              default=AdManager.STAUTS_EDITING,
                                              verbose_name='状态')
    mark = models.CharField(max_length=120, default='', verbose_name='备注')

    objects = AdManager()

    class Meta:
        db_table = 'beep_ad'
        ordering = ['-expired_at']
        verbose_name = '广告'
        verbose_name_plural = '广告'


mm_Ad = Ad.objects
