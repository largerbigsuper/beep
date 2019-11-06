import uuid
import datetime
from datetime import date

from django.db import models
from django.db.models import F
from django.conf import settings

from utils.modelmanager import ModelManager

class SearchTaskManager(ModelManager):
    
    def new_task(self):

        create_at = datetime.datetime.now()
        params = {
            'create_at': create_at,
            'slug': uuid.uuid4().__str__()
        }
        task = self.create(**params)
        return task

class SearchTask(models.Model):
    """搜索任务id
    """

    create_at = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    end_at = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    slug = models.CharField(max_length=120, unique=True, db_index=True, verbose_name='任务id')
    status = models.PositiveIntegerField(default=0, verbose_name='开始|完成|失败')

    objects = SearchTaskManager()

    class Meta:
        db_table = 'search_task'
        ordering = ['-id']

    def __str__(self):
        return self.slug

class SearchHistoryManager(ModelManager):

    def add_history(self, content, user_id=None):
        """增加记录
        """
        history = self.create(user_id=user_id, content=content)
        # 进行分词提取搜索关键字
        mm_SearchKeyWord.process_search(content)

        return history


class SearchHistory(models.Model):
    """搜索历史
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='用户')
    content = models.CharField(max_length=200, verbose_name='内容')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    objects = SearchHistoryManager()

    class Meta:
        db_table = 'search_history'
        ordering = ['-create_at']


class SearchKeyWordManager(ModelManager):

    def add_keyword(self, keyword):
        today = date.today()
        # obj, created = self.get_or_create(
        #     keyword=keyword, create_at__year=today.year, create_at__month=today.month, create_at__day=today.day)
        obj, created = self.get_or_create(keyword=keyword)
        if not created:
            obj.frequency = F('frequency') + 1
            obj.save()

    def process_search(self, content):
        if not content:
            return
        self.add_keyword(content)
        # seg_list = settings.JIEBA.cut(content)
        # keyword_list = [word for word in seg_list if len(word) > 1]
        # for keyword in keyword_list:
        #     self.add_keyword(keyword)


class SearchKeyWord(models.Model):
    """搜索关键字
    """

    keyword = models.CharField(max_length=40, verbose_name='关键字')
    frequency = models.PositiveIntegerField(default=1, verbose_name='检索次数')
    create_at = models.DateField(auto_now_add=True, verbose_name='记录时间')
    objects = SearchKeyWordManager()

    class Meta:
        db_table = 'search_keyword'
        unique_together = [
            ['keyword', 'create_at']
        ]
        ordering = ['-create_at', '-frequency']
        verbose_name = verbose_name_plural = '搜索关键词'


class HotSearchManager(ModelManager):

    LABEL_TYPE_NORMALE = 0
    LABEL_TYPE_HOT = 1
    LABEL_TYPE_NEW = 2
    LABEL_TYPE_RECOMMAND = 3
    LABEL_CHOICES = (
        (LABEL_TYPE_NORMALE, '普通'),
        (LABEL_TYPE_HOT, '热'),
        (LABEL_TYPE_NEW, '新'),
        (LABEL_TYPE_RECOMMAND, '荐'),
    )

    def hot(self):
        """热搜榜
        """
        task = mm_SearchTask.filter(status=1).first()
        if task:
            return self.filter(task=task)
        else:
            return self.filter(task=None)


class HotSearch(models.Model):
    """热门搜索
    """

    keyword = models.CharField(max_length=40, verbose_name='检索内容')
    frequency = models.PositiveIntegerField(default=1, verbose_name='检索次数')
    create_at = models.DateField(blank=True, verbose_name='产生时间')
    update_at = models.DateTimeField(blank=True, verbose_name='更新时间')
    is_top = models.BooleanField(default=False, verbose_name='置顶')
    lable_type = models.PositiveIntegerField(choices=HotSearchManager.LABEL_CHOICES,
                                             default=HotSearchManager.LABEL_TYPE_NORMALE,
                                             verbose_name='热|新|荐')
    task = models.ForeignKey(SearchTask, on_delete=models.SET_NULL, null=True, verbose_name='计算任务')

    objects = HotSearchManager()

    class Meta:
        db_table = 'hot_search'
        unique_together = [
            ['keyword', 'update_at']
        ]
        ordering = ['-task', '-update_at', '-frequency']
        verbose_name = verbose_name_plural = '热搜榜'


mm_SearchTask = SearchTask.objects
mm_SearchHistory = SearchHistory.objects
mm_SearchKeyWord = SearchKeyWord.objects
mm_HotSearch = HotSearch.objects
