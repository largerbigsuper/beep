from rest_framework import serializers
from django.db.models import F

from beep.users.serializers import UserBaseSerializer
from beep.common.serializers import AreaSerializer
from .models import (Activity, mm_Activity,
                     Registration)


class ActivityCreateSerializer(serializers.ModelSerializer):

    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ('id', 'user', 'title', 'cover', 'activity_type',
                  'start_at', 'end_at', 'ticket_price',
                  'area', 'address', 'live_plateform',
                  'live_address', 'total_user', 'contact_name',
                  'contact_info', 'total_view', 'total_registration',
                  'create_at', 'content'
                  )
        read_only_fields = ('user', 'total_view', 'total_registration')


class ActivityListSerializer(ActivityCreateSerializer):

    area = AreaSerializer()

    class Meta(ActivityCreateSerializer.Meta):
        pass


class ActivitySimpleSerializer(ActivityCreateSerializer):

    class Meta:
        model = Activity
        fields = ('id', 'title', 'cover', 'activity_type',
                  'start_at', 'end_at', 'ticket_price',
                  'area', 'address', 'live_plateform',
                  'live_address', 'total_user',
                  'total_view', 'total_registration',
                  'create_at', 'content'
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
