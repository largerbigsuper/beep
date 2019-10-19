from django.contrib import admin

from .models import Topic


class TopicAdmin(admin.ModelAdmin):
    pass

admin.register(Topic, TopicAdmin)
