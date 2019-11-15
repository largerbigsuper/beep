from django.contrib import admin

from .models import News, CrawledDocument, mm_News


def make_news_published(modeladmin, request, queryset):
    """文章发布
    """
    queryset.update(status=mm_News.STATUS_PUBLISHED)
make_news_published.short_description = '发布'

def make_news_recall(modeladmin, request, queryset):
    """文章撤回
    """
    queryset.update(status=mm_News.STATUS_RECALL)
make_news_recall.short_description = '撤回'
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at', 'status']
    actions = [make_news_published, make_news_recall]

@admin.register(CrawledDocument)
class CrawledDocumentAdmin(admin.ModelAdmin):
    
    list_display = [f.name for f in CrawledDocument._meta.get_fields()]
