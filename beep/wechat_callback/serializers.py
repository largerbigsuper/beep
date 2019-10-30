from rest_framework import serializers

from .models import WxMessage

class WxMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = WxMessage
        fields = '__all__'
