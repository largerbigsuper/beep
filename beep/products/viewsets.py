from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction

from utils.serializers import NoneParamsSerializer
from beep.users.models import mm_Point

from .models import mm_Sku, mm_SkuExchange
from .filters import SkuFilter
from .serializers import SkuSerializer, SkuExchangeSerializer

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
            exchange= mm_SkuExchange.add_exchange(request.user.id, pk, sku.point)
            # 消费积分
            mm_Point.add_action(request.user.id, mm_Point.ACTION_SKU_EXCHANGE_PAY, amount=sku.point)
            # 更新产品数量统计
            mm_Sku.update_count_data(pk)

            return Response()

class SkuExchangeViewSet(viewsets.ModelViewSet):
    """兑换申请
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SkuExchangeSerializer

    def get_queryset(self):
        return mm_SkuExchange.filter(user=self.request.user)

