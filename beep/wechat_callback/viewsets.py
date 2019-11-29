from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import mm_WxMessage
from .filters import WxMessageFilter
from .serializers import WxMessageSerializer

from utils.exceptions import BeepException

class WxMessageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    queryset = mm_WxMessage.all()
    permission_classes = []
    serializer_class = WxMessageSerializer
    filter_class = WxMessageFilter

    def paginate_queryset(self, queryset):
        # a = queryset
        return super().paginate_queryset(queryset)

    
    @action(detail=False, methods=['get'])
    def get_history(self, request):
        """获取聊天记录
        """
        room_wxid = request.query_params.get('room_wxid')
        if not room_wxid:
            raise BeepException('room_wxid缺失')
        
        queryset = mm_WxMessage.filter(room_wxid=room_wxid)

        serialier = WxMessageSerializer(queryset, many=True)
        maybe_big_json = serialier.data
        return Response(data=maybe_big_json)
        