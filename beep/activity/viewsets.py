from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction

from .serializers import (ActivityCreateSerializer, ActivityListSerializer,
                          RegistrationCreateSerializer, RegistrationListSerializer,
                          CollectCreateSerializer, CollectListSerializer, MyCollectListSerializer
                          )
from .models import mm_Activity, mm_Registration, mm_Collect
from .filters import ActivityFilter, CollectFilter
from beep.blog.models import mm_Blog
from utils.permissions import IsOwerPermission


class ActivityViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = mm_Activity.all().select_related('user')
    filter_class = ActivityFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityListSerializer
        else:
            return ActivityCreateSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            activity = serializer.save(user=self.request.user)
            params = {
                'user': self.request.user,
                'cover': activity.cover,
                'title': '发布了活动：' + activity.title,
                'activity': activity
            }
            mm_Blog.create(**params)


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


class CollectViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet
                     ):
    """活动收藏
    create -- 添加活动收藏
    destory -- 删除收藏
    list -- 收藏人列表
    mine -- 我的收藏列表
    """

    filter_class = CollectFilter

    def get_permissions(self):
        permissions = []
        if self.action in ['create', 'destory', 'mine']:
            permissions.append(IsAuthenticated())
        if self.action in ['destory']:
            permissions.append(IsOwerPermission())
        return permissions

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectCreateSerializer
        elif self.action == 'mine':
            return MyCollectListSerializer
        else:
            return CollectListSerializer

    def get_queryset(self):
        queryset = mm_Collect.all()
        if self.action in ('mine'):
            queryset = queryset.filter(
                user=self.request.user).select_related('activity', 'activity__user')
        else:
            queryset = queryset.select_related('user', 'activity')
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        # 更新收藏统计
        mm_Activity.update_data(instance.activity_id, 'total_collect')
    
    def perform_destroy(self, instance):
        # 更新收藏统计
        mm_Activity.update_data(instance.activity_id, 'total_collect', -1)
        instance.delete()

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """我的收藏列表
        """

        return super().list(request)
