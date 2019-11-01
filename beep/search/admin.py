from django.contrib import admin

from .models import SearchKeyWord

@admin.register(SearchKeyWord)
class SearchKeyWordAdmin(admin.ModelAdmin):
    
    list_display = ['keyword', 'frequency', 'create_date']
    list_filter = ['create_date']
