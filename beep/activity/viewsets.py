from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (ActivityCreateSerializer, ActivityListSerializer,
                          RegistrationCreateSerializer, RegistrationListSerializer)
from .models import mm_Activity, mm_Registration
from .filters import ActivityFilter


class ActivityViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = mm_Activity.all()
    filter_class = ActivityFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityListSerializer
        else:
            return ActivityCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        mm_Activity.update_data(instance.id, 'total_view')
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class RegistrationViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    """报名

    create -- 报名
    list -- 我的报名列表
    destory -- 删除报名
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list']:
            return RegistrationListSerializer
        else:
            return RegistrationCreateSerializer
    
    def get_queryset(self):
        return mm_Registration.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        mm_Activity.update_data(instance.activity.id, 'total_registration')
        return super().perform_create(serializer)

    def perform_destroy(self, instance):
        mm_Activity.update_data(instance.activity_id, 'total_registration', -1)
        return super().perform_destroy(instance)
