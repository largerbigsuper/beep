from django.contrib import admin

from .models import Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'ad_type', 'blog', 'hotSearch', 'order_num', 'image', 'link', 'module_type', 'position_type', 'start_at', 'expired_at', 'status', 'mark']
    list_filter = ['status', 'ad_type', 'module_type', 'position_type']
    search_fields = ['mark', 'blog']
    autocomplete_fields = ['blog', 'hotSearch']