from collections import defaultdict

from django.db import transaction
from django.db.models import F, Count
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
                          CommentCreateSerializer, CommentListSerializer, CommentDetailSerializer,
                          LikeCreateSerializer, LikeListSerializer, MyLikeListSerializer,
                          CommentLikeCreateSerializer)
from .models import mm_Topic, mm_Blog, mm_AtMessage, mm_Like, mm_BlogShare, mm_Comment
from .filters import CommentFilter, LikeFilter, BlogFilter
from beep.search.models import mm_SearchHistory
from beep.users.models import mm_User



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
    add_like -- 添加点赞
    add_share -- 分享
    mine -- 我的博文列表
    following -- 我关注的博文列表
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
        if self.action in ['list']:
            queryset = queryset.select_related('user', 'topic').annotate(score=F('total_like') + F('total_comment') + F('total_view')).order_by('-score')
            # 处理搜索记录
            content = self.request.query_params.get('content__icontains', '')
            if content:
                user_id = None
                if self.request.user:
                    user_id = self.request.user.id
                mm_SearchHistory.add_history(content=content, user_id=user_id)
        elif self.action in ['mine']:
            queryset = queryset.select_related('topic')
        elif self.action in ['following']:
            following_ids = self.request.user.following_set.values_list('following_id', flat=True)
            queryset = queryset.filter(user_id__in=following_ids).select_related('user', 'topic')
        else:
            queryset = queryset.select_related('user', 'topic')

        return queryset

    def perform_destroy(self, instance):
        # 更新我的博客个数
        mm_User.update_data(instance.user.id, 'total_blog', -1)
        return super().perform_destroy(instance)

    def retrieve(self, request, *args, **kwargs):
        """博客详情
        """
        blog = self.get_object()
        mm_Blog.update_data(blog.id, 'total_view')
        if blog.topic:
            mm_Topic.filter(pk=blog.topic.id).update(total_view=F('total_view') + 1)
        serializer = self.get_serializer(blog)

        return Response(serializer.data)

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
            _, created = mm_Like.blogs().update_or_create(
                user=request.user, blog=blog)
            if created:
                mm_Blog.update_data(blog.id, 'total_like')

        return Response()

    @action(detail=True, methods=['delete'])
    def remove_like(self, request, pk=None):
        """取消点赞
        """
        blog = self.get_object()
        with transaction.atomic():
            mm_Blog.update_data(blog.id, 'total_like', -1)
            mm_Like.blogs().filter(user=request.user, blog=blog).delete()
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
                mm_Blog.update_data(blog.id, 'total_share')

        return Response()

    @action(detail=False, )
    def following(self, request):
        return super().list(request)


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
        elif self.action in ['mine', 'received']:
            return CommentDetailSerializer
        else:
            return CommentListSerializer

    def get_queryset(self):
        queryset = mm_Comment.all().select_related(
            'user', 'blog', 'blog__user', 'to_user', 'reply_to')

        if self.action in ('mine'):
            queryset = queryset.filter(user=self.request.user)
        elif self.action in ('received'):
            queryset = queryset.filter(to_user=self.request.user)
        elif self.action in ('all'):
            queryset = queryset.filter(parent=None)
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

    @action(detail=False, methods=['get'])
    def all(self, request):
        """评论列表
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        data = serializer.data
        reply_dict = defaultdict(int)
        comments = [c.id for c in page]
        count_dict = mm_Comment.filter(parent_id__in=comments).values('parent_id').annotate(total_reply=Count('pk')).order_by('parent_id')
        for d in count_dict:
            reply_dict[d['parent_id']] = d['total_reply']

        for c in data:
            c['total_reply'] = reply_dict[c['id']]
        return self.get_paginated_response(data)


class LikeViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet
                      ):
    """博文点赞
    create -- 添加点赞
    destory -- 删除点赞
    list -- 点赞人列表
    mine -- 我的点赞列表
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
        elif self.action == 'to_comment':
            return CommentLikeCreateSerializer
        else:
            return LikeListSerializer

    def get_queryset(self):
        queryset = mm_Like.all()
        if self.action in ('mine'):
            queryset = queryset.exclude(comment_id__isnull=True).filter(
                user=self.request.user).select_related('blog', 'blog__topic', 'blog__user')
        else:
            queryset = queryset.select_related('user')
        return queryset

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """我的点赞
        """

        return super().list(request)

    @action(detail=False, methods=['post'], serializer_class=CommentLikeCreateSerializer)
    def to_comment(self, request):
        """评论点赞
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.comment:
            mm_Comment.update_data(instance.comment_id, 'total_like', -1)
        else:
            mm_Blog.update_data(instance.blog_id, 'total_like', -1)
        instance.delete()
        return Response()
