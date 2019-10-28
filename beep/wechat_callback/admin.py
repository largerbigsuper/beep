from django.contrib import admin

from .models import WxBot, WxGroup, WxUser, WxMessage


@admin.register(WxBot)
class WxBotAdmin(admin.ModelAdmin):
    
    list_display = ['wxid', 'wx_alias', 'nickname', 'nonce']

@admin.register(WxUser)
class WxUserAdmin(admin.ModelAdmin):
    
    list_display = ['wxid', 'wx_alias', 'nickname']

@admin.register(WxGroup)
class WxGroupAdmin(admin.ModelAdmin):
    
    list_display = ['room_wxid', 'name', 'owner_wxid', 'member_count']

@admin.register(WxMessage)
class WxMessageAdmin(admin.ModelAdmin):
    list_display = ['wxid_from', 'wxid_to', 'msg', ]
