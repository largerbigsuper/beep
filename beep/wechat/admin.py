from django.contrib import admin

from .models import WxTemplate, WxSubscription, WxSubMessage

@admin.register(WxTemplate)
class WxTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'vars_list']


@admin.register(WxSubscription)
class WxSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'wx_template', 'create_at']
    list_filter = ['wx_template']
    search_fileds = ['user__name']

@admin.register(WxSubMessage)
class WxSubMessageAdmin(admin.ModelAdmin):

    list_display = ['id', 'wx_template', 'activity', 'news', 'status', 'data', 'create_at']
    list_filter = ['wx_template']
    search_fields = ['data']
