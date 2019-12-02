from django.contrib import admin

from .models import AutoFollowingCfg


@admin.register(AutoFollowingCfg)
class AutoFollowingCfgAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'user']

    autocomplete_fields = ['user']