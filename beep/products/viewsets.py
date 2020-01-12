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
