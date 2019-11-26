from rest_framework import serializers
from django.db.models import F

from beep.users.serializers import UserBaseSerializer, UserSampleSerializer
from beep.common.serializers import AreaSerializer
from .models import (Activity, mm_Activity,
                     Registration, mm_Registration,
                     Collect, mm_Collect,
                     RewardPlan, mm_RewardPlan,
                     RewardPlanApply, mm_RewardPlanApply,
                     Schedule, WxForm
                     )


class RewardPlanCreateSerializer(serializers.ModelSerializer):
    """奖励详情
    """
    coin_logo_url = serializers.CharField(write_only=True, allow_blank=True, required=False)
    class Meta:
        model = RewardPlan
        fields = ['desc', 'coin_name', 'coin_logo', 'coin_logo_url', 'total_coin', 'total_luckyuser', 'start_time']
        read_only_fields = ['coin_logo']
class RewardPlanSerializer(serializers.ModelSerializer):
    """奖励详情
    """
    result = serializers.ListField()
    is_applyed = serializers.SerializerMethodField()
    coin_logo = serializers.SerializerMethodField()
    
    def get_coin_logo(self, obj):
        if obj.coin_logo:
            return obj.coin_logo.url
        else:
            return ''

    def get_is_applyed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(self, '_applys'):
            self._applys = mm_RewardPlanApply.filter(user=user).values_list('rewardplan_id', flat=True)
        return 1 if obj.id in self._applys else 0
    class Meta:
        model = RewardPlan
        fields = ['id', 'desc', 'coin_name', 'coin_logo', 'total_coin', 'total_luckyuser', 'start_time', 'applyers', 'result', 'is_applyed']


class ActivityCreateSerializer(serializers.ModelSerializer):

    user = UserBaseSerializer(read_only=True)
    cover_url = serializers.CharField(write_only=True, allow_blank=True, required=False)

    rewardplan = RewardPlanCreateSerializer(allow_null=True, required=False)

    class Meta:
        model = Activity
        # rewardplan_fields = ['coin_name', 'coin_logo', 'total_coin', 'total_luckyuser', 'start_time']
        fields = ['id', 'user', 'title', 'cover', 'activity_type',
                  'start_at', 'end_at', 'ticket_price',
                  'address', 'coordinates', 'live_plateform',
                  'live_address', 'total_user', 'contact_name',
                  'contact_info', 'total_view', 'total_registration',
                  'create_at', 'content', 'total_collect',
                  'province_code', 'province_name',
                  'city_code', 'city_name',
                  'district_code', 'district_name', 'blog_id', 'cover_url', 'summary_id'] + ['rewardplan']
        read_only_fields = ('user', 'total_view', 'total_registration', 'total_collect', 'blog_id', 'cover', 'summary_id')


class ActivityListSerializer(ActivityCreateSerializer):

    is_registrated = serializers.SerializerMethodField()
    is_collected = serializers.SerializerMethodField()
    rewardplan = RewardPlanSerializer()

    def get_is_registrated(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(user, '_activitys'):
            user._activitys = mm_Registration.filter(user=user).values_list('activity_id', flat=True)
        return 1 if obj.id in user._activitys else 0

    def get_is_collected(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(user, '_collected_activitys'):
            user._collected_activitys = mm_Collect.filter(user=user).values_list('activity_id', flat=True)
        return 1 if obj.id in user._collected_activitys else 0

    class Meta:
        model = Activity
        fields = ('id', 'user', 'title', 'cover', 'activity_type',
                  'start_at', 'end_at', 'ticket_price',
                  'address', 'coordinates', 'live_plateform',
                  'live_address', 'total_user', 'contact_name',
                  'contact_info', 'total_view', 'total_registration',
                  'create_at', 'content', 'is_registrated', 'total_collect', 'is_collected',
                  'province_code', 'province_name',
                  'city_code', 'city_name',
                  'district_code', 'district_name', 'blog_id', 'wx_groupname', 'wx_groupwxid', 'wx_botwxid',
                  'ask_allowed', 'rewardplan', 'summary_id'
                  )


class ActivitySimpleSerializer(ActivityCreateSerializer):

    class Meta:
        model = Activity
        fields = ('id', 'title', 'cover', 'activity_type',
                  'start_at', 'end_at', 'ticket_price',
                  'address', 'coordinates', 'live_plateform',
                  'live_address', 'total_user',
                  'total_view', 'total_registration',
                  'create_at', 'content', 'total_collect',
                  'province_code', 'province_name',
                  'city_code', 'city_name',
                  'district_code', 'district_name', 'blog_id'
                  )


class RegistrationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = ['id', 'activity', 'company', 'address', 'name', 'phone']


class RegistrationListSerializer(serializers.ModelSerializer):

    activity = ActivitySimpleSerializer()

    class Meta:
        model = Registration
        fields = ['id', 'activity', 'status', 'create_at']



class CollectCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collect
        fields = ('id', 'activity', 'create_at')

class CollectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collect
        fields = ('id', 'user', 'create_at')


class MyCollectListSerializer(serializers.ModelSerializer):

    activity = ActivitySimpleSerializer()

    class Meta:
        model = Collect
        fields = ('id', 'activity', 'create_at')


class RewardPlanApplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardPlanApply
        fields = ['rewardplan', 'address',]

class RewardPlanApplySerializer(serializers.ModelSerializer):

    rewardplan = RewardPlanSerializer()
    class Meta:
        model = RewardPlanApply
        fields = ['id', 'rewardplan', 'activity', 'address', 'create_at', 'is_selected']


class RewardPlanApplyListSerializer(serializers.ModelSerializer):

    user = UserSampleSerializer()

    class Meta:
        model = RewardPlanApply
        fields = ['id', 'user', 'address', 'create_at', 'is_selected']


# ========= Schedule Serializers  ==========


class ScheduleSerializer(serializers.ModelSerializer):

    activity = ActivityListSerializer(read_only=True)
    class Meta:
        model = Schedule
        fields = ['id', 'plan_datetime', 'content', 'create_at', 'activity']

class WxFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = WxForm
        fields = ['id', 'wxform_id']
    