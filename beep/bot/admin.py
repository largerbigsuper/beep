# -*- coding: utf-8 -*-
from django.contrib import admin, messages

from .models import BotName, BotNameBuilder, BotAvatar, BotAvatarBuilder, BotBuilder, Bot, BotComment, BotTask
from beep.users.models import User
from django.db import IntegrityError
from django.utils.safestring import mark_safe


@admin.register(BotName)
class BotNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'used')
    list_filter = ('used',)


@admin.register(BotNameBuilder)
class BotNameBuilderAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'done', 'create_at')
    list_filter = ('done', 'create_at')

    actions = ['make_import']

    def make_import(self, request, queryset):
        for obj in queryset:
            if obj.done:
                continue
            instances = []
            values = obj.text.split('\r').split('\n')
            for value in values:
                if value:
                    value = value.strip()
                    instances.append(BotName(text=value))
            if instances:
                BotName.objects.bulk_create(instances)
            obj.done = True
            obj.save()

    make_import.short_description = '导入'


@admin.register(BotAvatar)
class BotAvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'image_tag', 'used')
    list_filter = ('used',)

    def image_tag(self, obj):
        return mark_safe('<img src="{}" width="80" height="80" />'.format(obj.text))

    image_tag.short_description = '图片'


@admin.register(BotAvatarBuilder)
class BotAvatarBuilderAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'done', 'create_at')
    list_filter = ('done', 'create_at')

    actions = ['make_import']

    def make_import(self, request, queryset):
        for obj in queryset:
            if obj.done:
                continue
            instances = []
            values = obj.text.split('\r').split('\n')
            for value in values:
                if value:
                    value = value.strip()
                    instances.append(BotAvatar(text=value))
            if instances:
                BotAvatar.objects.bulk_create(instances)
            obj.done = True
            obj.save()
    
    make_import.short_description = '导入'


@admin.register(BotBuilder)
class BotBuilderAdmin(admin.ModelAdmin):
    list_display = ('id', 'desc', 'total', 'done', 'results', 'create_at')
    list_filter = ('done', 'create_at')


    actions = ['make_import']

    def make_import(self, request, queryset):
        for obj in queryset:
            if obj.done:
                continue
            names = list(BotName.objects.filter(used=False).values())
            if len(names) < obj.total:
                messages.error(request, '可用账号名不足')
                return
            avatars = BotAvatar.objects.filter(used=False).values()
            if len(avatars) < obj.total:
                messages.error(request, '可用头像不足')
                return
            results = []
            skip_names = []
            for index in range(obj.total):
                name = names[index]
                username = 'bpb_' + name['text']
                avatar = avatars[index]['text']
                if User.objects.filter(username=username).exists():
                    skip_names.append(username)
                    continue
                user = User(username=username, account=username, avatar_url=avatar, name=username, is_bot=True)
                user.save()
                bot = Bot(user=user)
                bot.save()
                results.append({"user_id": user.id, "id": bot.id, "username": user.username})
                BotName.objects.filter(pk=names[index]['id']).update(used=True)
                BotAvatar.objects.filter(pk=avatars[index]['id']).update(used=True)

            obj.done = True
            obj.results = results
            obj.save()
            if skip_names:
                warning_msg = ''.join(skip_names) + '等名称有重复'
                messages.warning(request, warning_msg)
    
    make_import.short_description = '导入'

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'is_on',
        'create_at',
        'update_at',
    )
    list_filter = ('is_on', 'create_at', 'update_at')
    autocomplete_fields = ['user']


@admin.register(BotComment)
class BotCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'text')

@admin.register(BotTask)
class BotTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_open')
