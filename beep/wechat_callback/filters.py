from django_filters import rest_framework as filters


from .models import WxMessage
class WxMessageFilter(filters.FilterSet):

    class Meta:
        model = WxMessage
        fields = {
            'room_wxid': ['exact'],
            'msg_type': ['exact'],
            'user_type': ['exact'],
            'msg_timestamp': ['gt', 'lt'],
            'create_at': ['gt', 'lt'],
        }
