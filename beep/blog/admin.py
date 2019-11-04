from django.contrib import admin

from .models import Topic, Blog


class BlogAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'user', 'topic', 'is_anonymous', 'create_at', 'order_num']
    list_filter = ['topic__topic_type', 'topic', 'is_top']
    list_editable = ['order_num']

admin.site.register(Blog, BlogAdmin)


class TopicAdmin(admin.ModelAdmin):
      
    list_display = [f.name for f in Topic._meta.fields]
    list_filter = ['topic_type']

admin.site.register(Topic, TopicAdmin)
