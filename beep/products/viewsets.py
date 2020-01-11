from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction

from utils.serializers import NoneParamsSerializer
from beep.users.models import mm_Point

from .models import (mm_Sku, mm_SkuOrderItem, mm_SkuOrderAddress,
    SkuOrder, mm_SkuOrder, SkuCart, mm_SkuCart)
from .filters import SkuFilter
from .serializers import (SkuSerializer, SkuOrderSerializer, SkuOrderListSerializer,
    SkuOrderItemSerializer, SkuOrderAddressSerializer,
    SkuCartSerializer, SkuCartListSerialzier)

class SkuViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = mm_Sku.published_sku()
    filter_class = SkuFilter
    serializer_class = SkuSerializer

    @action(detail=True, methods=['post'], serializer_class=NoneParamsSerializer, permission_classes=[IsAuthenticated])
    def add_exchange(self, request, pk=None):
        """申请兑换
        """
        sku = self.get_object()
        # 判断积分情况
        total_point = mm_Point.get_total_point(request.user.id)
        if total_point < sku.point:
            data = {
                'detail': '积分不足'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            # 创建申请记录
            exchange= mm_SkuOrderItem.add_exchange(request.user.id, pk, sku.point)
            # 消费积分
            mm_Point.add_action(request.user.id, mm_Point.ACTION_SKU_EXCHANGE_PAY, amount=sku.point)
            # 更新产品数量统计
            mm_Sku.update_count_data(pk)

            return Response()


class SkuOrderViewSet(viewsets.ModelViewSet):
    """订单
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SkuOrderSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SkuOrderSerializer
        else:
            return SkuOrderListSerializer

    def get_queryset(self):
        return mm_SkuOrder.my_orders(user_id=self.request.user.id)

    def perform_destroy(self, instance):
        instance.user_del = True
        instance.save()

class SkuOrderItemViewSet(viewsets.ModelViewSet):
    """兑换申请
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SkuOrderItemSerializer

    def get_queryset(self):
        return mm_SkuOrderItem.filter(user=self.request.user)
    


class SkuOrderAddressViewSet(viewsets.ModelViewSet):
    """收货地址
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SkuOrderAddressSerializer

    def get_queryset(self):
        return mm_SkuOrderAddress.my_address(user_id=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_del = True
        instance.save()


class SkuCartViewSet(viewsets.ModelViewSet):
    """购物车
    """
    permission_classes = [IsAuthenticated]
    # serializer_class = SkuCartListSerialzier

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SkuCartSerializer
        else:
            return SkuCartListSerialzier

    def get_queryset(self):
        return mm_SkuCart.my_skucart(user_id=self.request.user.id)
