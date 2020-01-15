from rest_framework import serializers
from django.db import transaction
from django.db.models import F


from .models import (Sku, mm_Sku, SkuOrderItem, mm_SkuOrderItem,
        SkuProperty, SkuOrderAddress, SkuOrder, mm_SkuOrder, mm_SkuProperty,
        SkuCart, mm_SkuCart)
from beep.users.models import mm_Point

from utils.exceptions import BeepException
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
        
class SkuPropertyInlineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SkuProperty
        fields = ['id', 'property_name_1', 'property_value_1', 
        'property_name_2', 'property_value_2', 
        'property_name_3', 'property_value_3', 
        ]

class SkuSerializer(serializers.ModelSerializer):

    sku_properties = SkuPropertySerializer(many=True, read_only=True)

    class Meta:
        model = Sku
        fields = ['id', 'sku_type', 'name', 'cover', 'point', 'detail', 
        'total_left', 'create_at', 'sku_properties']


class SkuInlineSerializer(serializers.ModelSerializer):
    """购物车内商品详情
    """
    class Meta:
        model = Sku
        fields = ['id', 'sku_type', 'name', 'cover', 'point', 'detail', 'total_left', 'create_at']

class SkuOrderItemSerializer(serializers.ModelSerializer):

    sku = SkuInlineSerializer(read_only=True)
    class Meta:
        model = SkuOrderItem
        fields = ['id', 'sku', 'sku_property', 'quantity', 'point', 'status', 'create_at', 'update_at']
        read_only_fields = ['point', 'status', 'create_at', 'update_at']


class SkuOrderItemListSerializer(serializers.ModelSerializer):

    sku = SkuInlineSerializer(read_only=True)
    sku_property = SkuPropertyInlineSerializer(read_only=True)
    class Meta:
        model = SkuOrderItem
        fields = ['id', 'sku', 'sku_property', 'quantity', 'point', 'status', 'create_at', 'update_at']
        read_only_fields = ['point', 'status', 'create_at', 'update_at']

class SkuOrderSerializer(serializers.ModelSerializer):

    sku_order_items = SkuOrderItemSerializer(many=True)

    class Meta:
        model = SkuOrder
        fields = ['id', 'order_num', 'point', 'address', 'status', 'create_at', 'update_at', 'sku_order_items']
        read_only_fields = ['order_num', 'point', 'status', 'create_at', 'update_at']
        # write_only_fields = ['address_id']

    def create(self, validated_data):
        # """创建订单
        # json
        # {
        #     "address": 2,
        #     "sku_order_items": [
        #         {
        #             "sku_property": 6,
        #             "quantity": 2
        #         }
        #     ]
        # }
        # """
        request = self.context['request']
        sku_order_items = validated_data.pop('sku_order_items')
        order_num = mm_SkuOrder.get_order_num()
        point = 0
        for order_item_data in sku_order_items:
            sku_property = order_item_data['sku_property']
            sku = sku_property.sku
            quantity = order_item_data['quantity']
            # 判断库存
            if sku_property.total_left <= 0 or sku_property.total_left < order_item_data['quantity']:
                raise BeepException('库存不足')

            point += sku.point * quantity

        with transaction.atomic():
            # 生成总订单
            order = mm_SkuOrder.create(user=request.user, order_num=order_num, point=point, **validated_data)
            # 更新积分
            mm_Point.add_action(user_id=request.user.id, action=mm_Point.ACTION_SKU_EXCHANGE_PAY, amount=point)
            for order_item_data in sku_order_items:
                # 生成单个订单
                sku_property = order_item_data['sku_property']
                sku = sku_property.sku
                quantity = order_item_data['quantity']
                item_point = sku.point * quantity
                mm_SkuOrderItem.create(user=request.user, sku=sku, order=order, point=item_point, **order_item_data)
                # 更新产品库存
                mm_SkuProperty.filter(pk=sku_property.id).update(total_left=F('total_left') - quantity, total_sales=F('total_sales') + quantity)

            return order

class SkuOrderListSerializer(SkuOrderSerializer):

    sku_order_items = SkuOrderItemListSerializer(many=True)
    address = SkuOrderAddressSerializer(read_only=True)
    
    class Meta:
        model = SkuOrder
        fields = ['id', 'order_num', 'point', 'address', 'status', 'create_at', 'update_at', 'sku_order_items']
        read_only_fields = ['address', 'order_num', 'point', 'status', 'create_at', 'update_at']


class SkuCartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SkuCart
        fields = ['id', 'sku', 'sku_property', 'quantity', 'create_at']

    def create(self, validated_data):
        """创建购物车
        """
        request = self.context['request']
        user_id = request.user.id
        sku_id = validated_data['sku'].id
        sku_property_id = validated_data['sku_property'].id
        quantity = validated_data['quantity']
        return mm_SkuCart.add_sku(user_id, sku_id, sku_property_id, quantity)


class SkuCartListSerialzier(serializers.ModelSerializer):

    sku = SkuInlineSerializer()
    sku_property = SkuPropertySerializer()
    class Meta:
        model = SkuCart
        fields = ['id', 'sku', 'sku_property', 'quantity', 'create_at']
        read_only_fields = ['sku']
