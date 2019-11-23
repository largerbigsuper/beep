from rest_framework import serializers

from .models import WxSubscription

class WxSubscriptionSerializer(serializers.Serializer):
    """微信服务消息订阅
    """
    code = serializers.CharField(max_length=64)



