from django.contrib import admin

from .models import Topic, Blog, mm_Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'user', 'topic', 'is_anonymous', 'create_at', 'order_num']
    list_filter = ['topic__topic_type', 'topic', 'is_top']
    list_editable = ['order_num']

    def get_queryset(self, request):
        return mm_Blog.blogs()

    def delete_queryset(self, request, queryset):

        queryset.update(is_delete=True)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
      
    list_display = [f.name for f in Topic._meta.fields]
    list_filter = ['topic_type']

