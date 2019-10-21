from django.contrib import admin

from .models import Topic, Blog


class BlogAdmin(admin.ModelAdmin):
    pass

admin.site.register(Blog, BlogAdmin)


class TopicAdmin(admin.ModelAdmin):
    pass

admin.site.register(Topic, TopicAdmin)
