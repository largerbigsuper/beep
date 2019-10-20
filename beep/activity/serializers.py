from rest_framework import serializers
from django.db.models import F

from beep.users.serializers import UserBaseSerializer
from beep.common.serializers import AreaSerializer
from .models import (Activity, mm_Activity,
                     Registration, mm_Registration,
                     Collect, mm_Collect)


class ActivityCreateSerializer(serializers.ModelSerializer):

    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ('id', 'user', 'title', 'cover', 'activity_type',
                  'start_at', 'end_at', 'ticket_price',
                  'area', 'address', 'live_plateform',
                  'live_address', 'total_user', 'contact_name',
                  'contact_info', 'total_view', 'total_registration',
                  'create_at', 'content', 'total_collect'
                  )
        read_only_fields = ('user', 'total_view', 'total_registration', 'total_collect')


class ActivityListSerializer(ActivityCreateSerializer):

    area = AreaSerializer()
    is_registrated = serializers.SerializerMethodField()
    is_collected = serializers.SerializerMethodField()

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
                  'area', 'address', 'live_plateform',
                  'live_address', 'total_user', 'contact_name',
                  'contact_info', 'total_view', 'total_registration',
                  'create_at', 'content', 'is_registrated', 'total_collect', 'is_collected'
                  )


class ActivitySimpleSerializer(ActivityCreateSerializer):

    class Meta:
        model = Activity
        fields = ('id', 'title', 'cover', 'activity_type',
                  'start_at', 'end_at', 'ticket_price',
                  'area', 'address', 'live_plateform',
                  'live_address', 'total_user',
                  'total_view', 'total_registration',
                  'create_at', 'content', 'total_collect'
                  )


class RegistrationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = ['id', 'activity']


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