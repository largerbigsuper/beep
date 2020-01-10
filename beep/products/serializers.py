from rest_framework import serializers

from .models import Sku, SkuExchange, SkuProperty, SkuOrderAddress

class SkuOrderAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkuOrderAddress
        fields = ['id', 'name', 'phone', 'detail', 'create_at']
    
    def create(self, validated_data):
        request = self.context['request']
        instance = self.Meta.model(user=request.user, **validated_data)
        instance.save()
        return instance

class SkuPropertySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SkuProperty
        fields = ['id', 'property_name_1', 'property_value_1', 
        'property_name_2', 'property_value_2', 
        'property_name_3', 'property_value_3', 
        'total_left', 'total_sales']

class SkuSerializer(serializers.ModelSerializer):

    sku_properties = SkuPropertySerializer(many=True, read_only=True)

    class Meta:
        model = Sku
        fields = ['id', 'sku_type', 'name', 'cover', 'point', 'detail', 
        'total_left', 'create_at', 'sku_properties']


class SkuExchangeSerializer(serializers.ModelSerializer):

    sku = SkuSerializer()

    class Meta:
        model = SkuExchange
        fields = ['id', 'sku', 'point', 'status', 'create_at', 'update_at']
