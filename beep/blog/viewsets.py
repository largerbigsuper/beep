from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.serializers import NoneParamsSerializer
from utils.permissions import IsOwerPermission
from .serializers import (TopicSerializer, MyBlogSerializer, BlogSerialzier,
                          AtMessageSerializer,
                          CommentCreateSerializer, CommentListSerializer, MyCommentSerilizer, MyCommentCreateSerilizer,
                          BlogLikeSerializer,
                          LikeCreateSerializer, LikeListSerializer, MyLikeListSerializer)
from .models import mm_Topic, mm_Blog, mm_AtMessage, mm_BlogLike, mm_BlogShare, mm_Comment
from .filters import CommentFilter, LikeFilter


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    """话题
    """

    permission_classes = []
    serializer_class = TopicSerializer
    queryset = mm_Topic.allowed_topics()


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    """博客
    """

    permission_class = []
    serializer_class = BlogSerialzier
    queryset = mm_Blog.all().select_related('author', 'topic')

    @action(detail=True, methods=['post'], permission_class=[], serializer_class=NoneParamsSerializer)
    def add_like(self, request, pk=None):
        """点赞
        """
        blog = self.get_object()
        with transaction.atomic():
            _, created = mm_BlogLike.update_or_create(
                user=request.user, blog=blog)
            if created:
                blog.total_like = F('total_like') + 1
                blog.save()

        return Response()

    @action(detail=True, methods=['post'], permission_class=[], serializer_class=NoneParamsSerializer)
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

    @action(detail=True, methods=['post'], permission_class=[], serializer_class=CommentCreateSerializer)
    def add_comment(self, request, pk=None):
        """评论
        """
        blog = self.get_object()
        data = {}
        serailizer = self.serializer_class(data=request.data)
        if serailizer.is_valid():
            with transaction.atomic():
                reply_to = serailizer.validated_data['reply_to']
                if reply_to:
                    to_user = mm_Comment.get(pk=reply_to).user
                else:
                    to_user = request.user
                serailizer.save(user=request.user, blog=blog, to_user=to_user)
                blog.total_comment = F('total_comment') + 1
                blog.save()
                return Response()
        else:
            return Response(data=serailizer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], serializer_class=CommentListSerializer)
    def comments(self, request, pk=None):
        """评论列表
        """
        blog = self.get_object()
        queryset = mm_Comment.filter(
            blog=blog).select_related('user', 'to_user')
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MyBlogViewSet(viewsets.ModelViewSet):
    """我的博客
    """

    permission_class = [IsAuthenticated, ]
    serializer_class = MyBlogSerializer

    def get_queryset(self):

        queryset = mm_Blog.my_blogs(
            author_id=self.request.user.id).select_related('author', 'topic')

        return queryset


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
        return mm_AtMessage.my_messages(self.request.user.id).select_related('blog', 'blog__topic', 'blog__author')


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
            'user', 'blog', 'blog__author', 'to_user', 'reply_to')
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


class BlogLikeViewSet(mixins.CreateModelMixin,
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
        queryset = mm_BlogLike.all()
        if self.action in ('mine'):
            queryset = queryset.filter(
                user=self.request.user).select_related('blog', 'blog__topic', 'blog__author')
        else:
            queryset = queryset.select_related('user')
        return queryset

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """我的收藏
        """

        return super().list(request)
