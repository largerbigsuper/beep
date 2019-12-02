from rest_framework import serializers

from .models import Ad


class AdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = ('id', 'ad_type', 'order_num', 'image', 'link', 'module_type', 'position_type')

