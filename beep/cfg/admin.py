from django.contrib import admin

from .models import AutoFollowingCfg, ActionPointCfg


@admin.register(AutoFollowingCfg)
class AutoFollowingCfgAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'user']

    autocomplete_fields = ['user']


@admin.register(ActionPointCfg)
class ActionPointCfgAdmin(admin.ModelAdmin):
    
    list_display = ['code', 'name', 'point', 'max_per_day', 'is_on']