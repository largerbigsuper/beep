from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .models import mm_WxMessage
from .filters import WxMessageFilter
from .serializers import WxMessageSerializer

class WxMessageViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin):

        queryset = mm_WxMessage.all()
        permission_classes = []
        serializer_class = WxMessageSerializer
        filter_class = WxMessageFilter
