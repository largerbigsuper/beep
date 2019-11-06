from django.contrib import admin

from .models import SearchKeyWord, HotSearch, SearchHistory

@admin.register(SearchKeyWord)
class SearchKeyWordAdmin(admin.ModelAdmin):
    
    list_display = ['keyword', 'frequency', 'create_at']
    list_filter = ['create_at']


@admin.register(HotSearch)
class HotSearchAdmin(admin.ModelAdmin):

    list_display = ['id', 'keyword', 'frequency', 'is_top', 'lable_type', 'task']
    list_filter = ['is_top', 'lable_type']
