from django.contrib import admin

from .models import Activity, Registration, RewardPlan, RewardPlanApply
from .tasks import generate_activity_poster

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'cover', 'activity_type', 'start_at', 'end_at', 'is_recommand', 'status']
    search_fields = ['title']
    list_filter = ['activity_type', 'status', 'is_recommand']
    ordering = ['-create_at']

    def save_model(self, request, obj, form, change):
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
