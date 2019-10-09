from rest_framework import serializers


from beep.users.serializers import UserBaseSerializer
from beep.common.serializers import AreaSerializer
from .models import Activity, Registration

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

class ActivityListSerializer(serializers.ModelSerializer):

    area = AreaSerializer()

    class Meta(ActivityCreateSerializer.Meta):
        pass

