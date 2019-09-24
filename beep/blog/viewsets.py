from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.serializers import NoneParamsSerializer
from utils.permissions import IsOwerPermission
from .serializers import (TopicSerializer,
                          BlogCreateSerializer, BlogListSerialzier,
                          AtMessageSerializer,
                          CommentCreateSerializer, CommentListSerializer,
                          LikeCreateSerializer, LikeListSerializer, MyLikeListSerializer)
from .models import mm_Topic, mm_Blog, mm_AtMessage, mm_Like, mm_BlogShare, mm_Comment
from .filters import CommentFilter, LikeFilter, BlogFilter



class TopicViewSet(viewsets.ModelViewSet):
    """话题/专题
    list -- 专题榜
    """

    serializer_class = TopicSerializer
    queryset = mm_Topic.allowed_topics().select_related('user')

    def get_permissions(self):
        permissions = []
        if self.action in ['create', 'update', 'destory']:
            permissions = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permissions]


class BlogViewSet(viewsets.ModelViewSet):
    """博客
    list -- 博客列表
    update -- 修改博客
    destory -- 删除
    add_like -- 添加收藏
    add_share -- 分享
    mine -- 我的博文列表
    """

    filter_class = BlogFilter

    def get_permissions(self):

        permissions = []
        if self.action in ['add_like', 'add_share', 'mine']:
            permissions.append(IsAuthenticated())
        if self.action in ['update', 'destroy']:
            permissions.append(IsOwerPermission())
        return permissions

    def get_serializer_class(self):

        if self.action in ['create', 'update', 'mine']:
            return BlogCreateSerializer
        elif self.action in ['add_like', 'add_share']:
            return NoneParamsSerializer
        else:
            return BlogListSerialzier

    def get_queryset(self):
        queryset = mm_Blog.all()
        if self.action in ['mine']:
            queryset = queryset.select_related('topic')
        else:
            queryset = queryset.select_related('user', 'topic')
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """博客详情
        """
        response = super().retrieve(request, *args, **kwargs)
        blog = self.get_object()
        blog.total_view = F('total_view') + 1
        blog.save()
        blog.topic.total_view = F('total_view') + 1
        blog.topic.save()
        return response

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """我的博文列表
        """

        return super().list(request)

    @action(detail=True, methods=['post'])
    def add_like(self, request, pk=None):
        """点赞
        """
        blog = self.get_object()
        with transaction.atomic():
            _, created = mm_Like.update_or_create(
                user=request.user, blog=blog)
            if created:
                blog.total_like = F('total_like') + 1
                blog.save()

        return Response()

    @action(detail=True, methods=['post'])
    def add_share(self, request, pk=None):
        """分享
        """
        blog = self.get_object()
        with transaction.atomic():
            _, created = mm_BlogShare.update_or_create(
                user=request.user, blog=blog)
            if created:
                blog.total_share = F('total_share') + 1
                blog.save()

        return Response()

class AtMessageViewSet(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """@我的消息
    """

    permission_classes = [IsAuthenticated]
    serializer_class = AtMessageSerializer

    def get_queryset(self):
        return mm_AtMessage.my_messages(self.request.user.id).select_related('blog', 'blog__topic', 'blog__user')


class CommentViewSet(viewsets.ModelViewSet):
    """所有评论接口
    create -- 添加／回复评论
    list -- 所有评论列表
    mine -- 我的评论列表
    update -- 修改评论
    desory -- 删除评论
    recivied -- 收到的评论
    """
    filter_class = CommentFilter

    def get_permissions(self):
        permissions = []
        if self.action in ('mine', 'received'):
            permissions.append(IsAuthenticated())
        if self.action in ['update', 'destroy']:
            permissions.append(IsOwerPermission())
        return permissions

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CommentCreateSerializer
        else:
            return CommentListSerializer

    def get_queryset(self):
        queryset = mm_Comment.all().select_related(
            'user', 'blog', 'blog__user', 'to_user', 'reply_to')

        if self.action in ('mine'):
            queryset = queryset.filter(user=self.request.user)
        elif self.action in ('received'):
            queryset = queryset.filter(to_user=self.request.user)
        return queryset

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """发出的评论
        """

        return super().list(request)

    @action(detail=False, methods=['get'])
    def received(self, request):
        """收到的评论
        """

        return super().list(request)


class LikeViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet
                      ):
    """博文收藏
    create -- 添加收藏
    destory -- 删除收藏
    list -- 收藏人列表
    mine -- 我的收藏列表
    """

    filter_class = LikeFilter

    def get_permissions(self):
        permissions = []
        if self.action in ['create', 'destory', 'mine']:
            permissions.append(IsAuthenticated())
        if self.action in ['destory']:
            permissions.append(IsOwerPermission())
        return permissions

    def get_serializer_class(self):
        if self.action == 'create':
            return LikeCreateSerializer
        elif self.action == 'mine':
            return MyLikeListSerializer
        else:
            return LikeListSerializer

    def get_queryset(self):
        queryset = mm_Like.all()
        if self.action in ('mine'):
            queryset = queryset.filter(
                user=self.request.user).select_related('blog', 'blog__topic', 'blog__user')
        else:
            queryset = queryset.select_related('user')
        return queryset

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """我的收藏
        """

        return super().list(request)
