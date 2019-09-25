from datetime import date

from django.db import models
from django.db.models import F
from django.conf import settings

from utils.modelmanager import ModelManager

class SearchHistoryManager(ModelManager):

    def add_history(self, content, user_id=None):
        """增加记录
        """
        history = self.create(user_id=user_id, content=content)
        #TODO 进行分词提取搜索关键字
        #  
        return history


class SearchHistory(models.Model):
    """搜索历史
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='用户')
    content = models.CharField(max_length=200, verbose_name='内容')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    objects = SearchHistoryManager()

    class Meta:
        db_table = 'search_history'
        ordering = ['-create_at']


class SearchKeyWordManager(ModelManager):
    
    def add_keyword(self, keyword):
        obj, created = self.get_or_create(keyword=keyword, create_date=date.today())
        if not created:
            obj.frequency = F('frequency') + 1
            obj.save()


class SearchKeyWord(models.Model):
    """搜索关键字
    """
    
    keyword = models.CharField(max_length=40, verbose_name='关键字')
    frequency = models.PositiveIntegerField(default=1, verbose_name='检索次数')
    create_date = models.DateField(auto_now_add=True, verbose_name='记录时间')
    objects = SearchKeyWordManager()

    class Meta:
        db_table = 'search_keyword'
        unique_together = [
            ['keyword', 'create_date']
        ]
        ordering = ['-create_date', '-frequency']



mm_SearchHistory = SearchHistory.objects
mm_SearchKeyWord = SearchKeyWord.objects
