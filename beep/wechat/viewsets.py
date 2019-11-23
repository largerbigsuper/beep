from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from .models import mm_WxSubscription
from .serializers import WxSubscriptionSerializer


class WxSubscriptionViewSet(mixins.CreateModelMixin,
                            GenericViewSet):

    queryset = mm_WxSubscription.all()
    serializer_class = WxSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        obj = mm_WxSubscription.add_subscription(user=request.user, code=code)
        if obj:
            return Response()
        else:
            raise ParseError('未知模版id: {}'.format(code))
