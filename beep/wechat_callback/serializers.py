from rest_framework import serializers

from .models import WxMessage, mm_WxUser
from beep.users.models import mm_User

class WxMessageSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField(method_name='get_user')

    def get_user(self, obj):
        if obj.user_type == 0:
            info = mm_WxUser.get_info(obj.wxid_from)
        else:
            info = mm_User.get_info(obj.user_id)
        return info

    class Meta:
        model = WxMessage
        wxmessage_fields = [f.name for f in WxMessage._meta.get_fields()]
        fields = wxmessage_fields + ['user']
