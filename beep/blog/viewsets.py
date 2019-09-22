from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.serializers import NoneParamsSerializer
from .serializers import (TopicSerializer, MyBlogSerializer, BlogSerialzier,
                          AtMessageSerializer, 
                          CommentCreateSerializer, CommentSerializer,
                          BlogLikeSerializer)
from .models import mm_Topic, mm_Blog, mm_AtMessage, mm_BlogLike, mm_BlogShare, mm_Comment


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
            _, created = mm_BlogLike.update_or_create(user=request.user, blog=blog)
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
            _, created = mm_BlogShare.update_or_create(user=request.user, blog=blog)
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

    @action(detail=True, methods=['get'], serializer_class=CommentSerializer)
    def comments(self, request, pk=None):
        """评论列表
        """
        blog = self.get_object()
        queryset = mm_Comment.filter(blog=blog).select_related('user', 'to_user')
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


class MyBlogLikeViewSet(mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet, ):
    """我的收藏
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BlogLikeSerializer

    def get_queryset(self):
        return mm_BlogLike.filter(user=self.request.user).select_related('blog', 'blog__topic', 'blog__author')


# class MyCommentViewSet(viewsets.ModelViewSet):
#     """我的评论列表
#     """

#     permission_class = [IsAuthenticated]
#     serializer_class = 

#     def get_queryset(self)