from django.contrib import admin

from .models import News

class NewsAdmin(admin.ModelAdmin):
    pass


admin.register(News, NewsAdmin)

