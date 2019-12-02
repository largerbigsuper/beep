from django.contrib import admin

from .models import Topic, Blog, mm_Blog, Blog_Blog, Blog_Article
from .forms import Blog_ArticleAdminForm

from django.db import models

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'topic', 'get_content', 'is_anonymous', 'create_at', 'order_num']
    list_filter = ['topic__topic_type', 'topic', 'is_top']
    list_editable = ['order_num']
    search_fields = ['title', 'content']
    autocomplete_fields = ['user', 'topic']

    def get_queryset(self, request):
        return mm_Blog.select_related('topic', 'user').all()

    def delete_queryset(self, request, queryset):
        # FIXME 需要产生post_save信号
        for obj in queryset:
            obj.is_delete = True
            obj.save(update_fields=['is_delete'])

    def get_content(self, obj):
        return obj.content[:100]

    get_content.short_description = '内容'


@admin.register(Blog_Blog)
class Blog_BlogAdmin(BlogAdmin):

    def get_queryset(self, request):
        return mm_Blog.filter(title__isnull=True).select_related('topic', 'user').all()
    

@admin.register(Blog_Article)
class Blog_ArticleAdmin(BlogAdmin):
    form = Blog_ArticleAdminForm

    def get_queryset(self, request):
        return mm_Blog.filter(title__isnull=False).select_related('topic', 'user').all()


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
      
    list_display = ['id', 'name', 'sub_name', 'cover', 'topic_type', 'total_view', 'total_comment', 'total_blog', 'create_at', 'order_num']
    list_filter = ['topic_type']
    list_editable = ['order_num']
    search_fields = ['name', 'sub_name']


