from django.contrib import admin

from .models import Activity, Registration, RewardPlan, RewardPlanApply

class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'cover', 'activity_type', 'start_at', 'end_at']

admin.site.register(Activity, ActivityAdmin)

class RegistrationAdmin(admin.ModelAdmin):

    pass

admin.site.register(Registration, RegistrationAdmin)


@admin.register(RewardPlan)
class RewardPlanAdmin(admin.ModelAdmin):
    pass

@admin.register(RewardPlanApply)
class RewardPlanApplyAdmin(admin.ModelAdmin):
    search_fields = ['user__name', 'activity__title']
    list_filter = ['activity', 'rewardplan', 'is_selected']
