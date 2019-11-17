from django.contrib import admin

from .models import Topic, Blog, mm_Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'title', 'user', 'topic', 'get_content', 'is_anonymous', 'create_at', 'order_num']
    list_filter = ['topic__topic_type', 'topic', 'is_top']
    list_editable = ['order_num']
    search_fields = ['title']
    autocomplete_fields = ['topic']

    def get_queryset(self, request):
        return mm_Blog.select_related('topic', 'user').all()

    def delete_queryset(self, request, queryset):
        queryset.update(is_delete=True)

    def get_content(self, obj):
        return obj.content[:100]

    get_content.short_description = '内容'
    


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
      
    list_display = ['id', 'name', 'sub_name', 'cover', 'topic_type', 'total_view', 'total_comment', 'total_blog', 'create_at', 'order_num']
    list_filter = ['topic_type']
    list_editable = ['order_num']
    search_fields = ['name', 'sub_name']


