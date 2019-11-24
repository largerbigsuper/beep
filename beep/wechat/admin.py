from django.contrib import admin

from .models import WxTemplate, WxSubscription, WxSubMessage, mm_WxSubMessage

@admin.register(WxTemplate)
class WxTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'vars_list']


@admin.register(WxSubscription)
class WxSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'wx_template', 'create_at']
    list_filter = ['wx_template']
    search_fileds = ['user__name']


def make_published(modeladmin, request, queryset):
    for obj in queryset:
        mm_WxSubMessage.send(obj.id)
        obj.status = mm_WxSubMessage.STATUS_SEND
        obj.save()

make_published.short_description = '发布'
@admin.register(WxSubMessage)
class WxSubMessageAdmin(admin.ModelAdmin):

    list_display = ['id', 'wx_template', 'activity', 'hotsearch', 'title', 'warn_msg', 'status', 'create_at']
    list_filter = ['wx_template']
    search_fields = ['title', 'activity__title', 'hotsearch__keyword']
    autocomplete_fields = ['activity', 'hotsearch']

    actions = [make_published]
