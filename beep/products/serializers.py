from rest_framework import serializers

from .models import Sku, SkuExchange

class SkuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sku
        fields = ['id', 'name', 'cover', 'point', 'detail', 'total_left', 'create_at']


class SkuExchangeSerializer(serializers.ModelSerializer):

    sku = SkuSerializer()

    class Meta:
        model = SkuExchange
        fields = ['id', 'sku', 'point', 'status', 'create_at', 'update_at']
