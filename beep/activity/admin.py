from django.contrib import admin

from .models import Activity, Registration, RewardPlan, RewardPlanApply, mm_Activity
from .tasks import generate_activity_poster

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'cover', 'activity_type', 'start_at', 'end_at', 'is_recommand', 'status']
    search_fields = ['title']
    list_filter = ['activity_type', 'status', 'is_recommand']
    ordering = ['-create_at']

    def save_model(self, request, obj, form, change):
        # 更新直播群id
        if 'wx_groupwxid' in form.changed_data:
            # 移除上一个群直播状态
            _wx_groupwxid = form.initial['wx_groupwxid']
            wx_groupwxid = obj.wx_groupwxid
            live_groups = mm_Activity.cache.get(mm_Activity.key_live_rooms_activity_map, set())
            if _wx_groupwxid in live_groups:
                _live_room = live_groups[_wx_groupwxid]
                if obj.id in _live_room:
                    _live_room.remove(obj.id)
                    if _live_room:
                        live_groups[_wx_groupwxid] = _live_room
                    else:
                        del live_groups[_wx_groupwxid]
                    live_room = live_groups.get(wx_groupwxid, set())
                    live_room.add(obj.id)
                    live_groups[wx_groupwxid] = live_room
                    mm_Activity.cache.set(mm_Activity.key_live_rooms_activity_map, live_groups, 60*60*24*3)

        super().save_model(request, obj, form, change)
        # 生成海报
        generate_activity_poster.delay(obj.id)



@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'activity', 'status', 'create_at']
    search_fields = ['user__name']


@admin.register(RewardPlan)
class RewardPlanAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'desc', 'coin_name', 'coin_logo', 'total_coin', 'start_time']
    search_fields = ['desc']

@admin.register(RewardPlanApply)
class RewardPlanApplyAdmin(admin.ModelAdmin):
    search_fields = ['user__name', 'activity__title']
    list_filter = ['activity', 'rewardplan', 'is_selected']
