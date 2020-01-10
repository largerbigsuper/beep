import datetime
from collections import defaultdict, OrderedDict

from django.db import transaction
from django.db.models import F, Count, Q
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
                          CommentCreateSerializer, CommentSerializer, CommentListSerializer,
                          LikeCreateSerializer, LikeListSerializer, MyLikeListSerializer,
                          CommentLikeCreateSerializer)
from .models import mm_Topic, mm_Blog, mm_AtMessage, mm_Like, mm_BlogShare, mm_Comment, mm_user_Blog
from .filters import CommentFilter, LikeFilter, BlogFilter, TopicFilter
from beep.search.models import mm_SearchHistory
from beep.users.models import mm_User   
from beep.users.serializers import UserBaseSerializer
from beep.ad.models import mm_Ad
from utils.pagination import ReturnAllPagination, Size_10_Pagination



class TopicViewSet(viewsets.ModelViewSet):
    """话题/专题
    list -- 专题榜
    """

    serializer_class = TopicSerializer
    # queryset = mm_Topic.allowed_topics().select_related('user')
    filter_class = TopicFilter

    def get_permissions(self):
        permissions = []
        if self.action in ['create', 'update', 'destory']:
            permissions = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permissions]
    
    def get_queryset(self):
        queryset = mm_Topic.allowed_topics().select_related('user')
        if self.action in ['xinrenbang']:
            # 新人榜 按排序值排小的靠前，同排序值的按时间正序排
            queryset = queryset.filter(topic_type=mm_Topic.TYPE_XinRenBang).order_by('order_num', 'create_at')
        elif self.action in ['topic']:
            # 专题榜 按排序值排小的靠前，同排序值的按时间倒序排
            queryset = queryset.filter(topic_type=mm_Topic.TYPE_ZhuanTiBang).order_by('order_num', '-create_at')
        return queryset
    
    @action(detail=False)
    def lookup(self, request):
        """根据话题名获取话题详情
        """

        name = request.query_params.get('name')

        if name:
            topic = mm_Topic.filter(name=name).first()
            if topic:
                serializer = TopicSerializer(topic)
                data = serializer.data
                status_code = status.HTTP_200_OK
            else:
                data = {'detail': '需要参数name'}
                status_code = status.HTTP_404_NOT_FOUND
        else:
            data = {'detail': '需要参数name'}
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=status_code)


    @action(detail=False)
    def topic(self, request):
        """专题榜
        """
        return super().list(request)

    @action(detail=False)
    def xinrenbang(self, request):
        """新人榜
        """
        return super().list(request)



class BlogViewSet(viewsets.ModelViewSet):

    """博客
    list -- 博客列表
    update -- 修改博客
    destory -- 删除
    add_like -- 添加点赞
    remove_like -- 删除点赞
    add_share -- 分享
    mine -- 我的博文列表
    following -- 我关注的博文列表
    """

    filter_class = BlogFilter

    def get_permissions(self):
        permissions = []
        if self.action in ['add_like', 'remove_like', 'add_share', 'mine', 'create', 'following']:
            permissions.append(IsAuthenticated())
        if self.action in ['update', 'destroy', 'remove_top', 'set_top']:
            permissions.append(IsOwerPermission())
        return permissions

    def get_serializer_class(self):

        if self.action in ['create', 'update']:
            return BlogCreateSerializer
        elif self.action in ['add_like', 'add_share']:
            return NoneParamsSerializer
        else:
            return BlogListSerialzier

    def get_queryset(self):
        queryset = mm_user_Blog.all().order_by('-is_top', '-id')
        if self.action == 'index':
            create_at_after = datetime.datetime.today() - datetime.timedelta(days=2)
            queryset = queryset.filter(create_at__gt=create_at_after).exclude(activity__isnull=False)
        if self.action in ['index', 'search']:
            # FIXME 
            # 搜索关联话题表
            # 后台修改博文关联的话题，但不修改话题内容导致搜索入口有搜索相关话题时，可能导致改博文不能被检索到
            content = self.request.query_params.get('q', '')
            if content:
                queryset = queryset.filter(Q(topic__name__icontains=content) | Q(title__icontains=content) | Q(content__icontains=content))
            queryset = queryset.exclude(origin_blog__is_delete=True).select_related('user', 'topic', 'topic__user').annotate(score=F('total_like') + F('total_comment') + F('total_view')).order_by('-score', '-create_at')
            # 处理搜索记录
            content = self.request.query_params.get('q', '')
            if content:
                user_id = None
                if self.request.user:
                    user_id = self.request.user.id
                mm_SearchHistory.add_history(content=content, user_id=user_id)
        elif self.action in ['mine', 'set_top']:
            queryset = queryset.filter(user=self.request.user).select_related('user', 'topic')
        elif self.action in ['following']:
            following_ids = self.request.user.following_set.values_list('following_id', flat=True)
            queryset = queryset.exclude(is_anonymous=True).filter(user_id__in=following_ids).select_related('user', 'topic')
        elif self.action in ['lookup']:
            queryset = queryset.exclude(is_anonymous=True).select_related('user', 'topic')
        elif self.action in ['topic']:
            queryset = queryset.filter(topic__topic_type=1).select_related('user', 'topic').order_by('order_num', '-create_at')
        elif self.action in ['xinrenbang']:
            queryset = queryset.filter(topic__topic_type=2).select_related('user', 'topic').order_by('order_num', 'create_at')
        else:
            queryset = queryset.select_related('user', 'topic')

        return queryset

    def perform_destroy(self, instance):
        # FIXME 数据同步在signals.py中
        instance.is_delete = True
        instance.save(update_fields=['is_delete'])

    def retrieve(self, request, *args, **kwargs):
        """博客详情
        """
        blog = self.get_object()
        mm_Blog.update_data(blog.id, 'total_view')
        if blog.topic:
            mm_Topic.filter(pk=blog.topic.id).update(total_view=F('total_view') + 1)
        serializer = self.get_serializer(blog)

        return Response(serializer.data)

    @action(detail=False)
    def search(self, request):
        """返回增加搜素用户
        """
        q = request.query_params.get('q', '')
        page_num = int(request.query_params.get('page', 1))
        if q and page_num == 1:
            user_qs = mm_User.filter(name__icontains=q)
            total_user = user_qs.count()
            top_ten = user_qs[:10]
            users_serializers = UserBaseSerializer(top_ten, many=True, context={'request': request})
            user_data = {
                'total': total_user,
                'data': users_serializers.data
            }
        else:
            user_data = {
                'total': 0,
                'data': []
            }

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        ad_blog_dict = mm_Ad.get_blog_hot_ad()
        if page_num == 1 and self.action == 'index':
            ad_blog_dict = mm_Ad.get_blog_hot_ad()
            if ad_blog_dict:
                ad_blog_ids = {ad_blog.id for ad_blog in ad_blog_dict.values()}
                _page = [obj for obj in page if obj.id not in ad_blog_ids]
                ads = sorted(ad_blog_dict.items())
                for index, blog in ads:
                    if index < 1:
                        continue
                    idx = index - 1
                    if len(_page) >= index:
                        _page.insert(idx, blog)
                page = _page
            
        serializer = self.get_serializer(page, many=True)

        # 自定义返回
        data = serializer.data
        return Response(OrderedDict([
            ('count', self.paginator.page.paginator.count),
            ('next', self.paginator.get_next_link()),
            ('previous', self.paginator.get_previous_link()),
            ('page_count', self.paginator.page.paginator.num_pages),
            ('results', data),
            ('users', user_data),
        ]))

    @action(detail=False, methods=['get'])
    def index(self, request):
        """我的博文列表
        """
        return self.search(request)

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """我的博文列表
        """
        return super().list(request)

    @action(detail=False, methods=['get'])
    def lookup(self, request):
        """某人博文列表
        """
        return super().list(request)

    @action(detail=False, methods=['get'])
    def topic(self, request):
        """专题榜博文列表，
        """
        return super().list(request)

    @action(detail=False, methods=['get'])
    def xinrenbang(self, request):
        """新人榜博文列表，
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
        """我的关注博文列表
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        page_num = int(request.query_params.get('page', 1))
        if page_num == 1:
            ad_blog = mm_Ad.get_blog_following_ad(request.user.id)
            if ad_blog:
                _page = [obj for obj in page if obj.id != ad_blog.id]
                page = [ad_blog] + _page
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def set_top(self, request, pk=None):
        """设置置顶
            
            只保留一个置顶
        """
        request.user.blog_set.filter(is_top=True).update(is_top=False)
        blog = self.get_object()
        blog.is_top = True
        blog.save()
        return Response()

    @action(detail=True, methods=['post'])
    def remove_top(self, request, pk=None):
        """取消置顶
 
        """
        request.user.blog_set.filter(is_top=True).update(is_top=False)
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
        queryset = mm_AtMessage.recevied(self.request.user.id).select_related('blog', 'blog__topic', 'blog__user', 'user')
        # 更新未读
        mm_AtMessage.recevied(self.request.user.id, status=mm_AtMessage.STATUS_CREATED).update(status=mm_AtMessage.STATUS_READED)
        return queryset


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
    pagination_class = ReturnAllPagination

    def get_permissions(self):
        permissions = []
        if self.action in ['mine', 'received', 'create']:
            permissions.append(IsAuthenticated())
        if self.action in ['update', 'destroy']:
            permissions.append(IsOwerPermission())
        return permissions

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CommentCreateSerializer
        elif self.action in ['received']:
            return CommentListSerializer
        else:
            return CommentSerializer

    def get_queryset(self):
        queryset = mm_Comment.all().select_related(
            'user', 'blog', 'blog__user', 'to_user', 'reply_to')

        if self.action in ('mine'):
            queryset = queryset.filter(user=self.request.user)
        elif self.action in ['received']:
            queryset = queryset.filter(to_user=self.request.user)
        elif self.action in ('all'):
            queryset = queryset.filter(parent=None)
        elif self.action in ['list']:
            queryset = queryset[:10]
        return queryset

    @action(detail=False, methods=['get'], pagination_class=Size_10_Pagination)
    def mine(self, request):
        """发出的评论
        """

        return super().list(request)

    @action(detail=False, methods=['get'], pagination_class=Size_10_Pagination)
    def received(self, request):
        """收到的评论
        """
        # 设置消息已读
        queryset = self.filter_queryset(self.get_queryset())
        queryset.filter(status=mm_Comment.STATUS_CREATED).update(status=mm_Comment.STATUS_READED)
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
    received -- 我收到的点赞列表
    """

    filter_class = LikeFilter

    def get_permissions(self):
        permissions = []
        if self.action in ['create', 'destory', 'mine', 'recivied']:
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
            queryset = queryset.filter(
                blog_id__gt=0,
                user=self.request.user).select_related('blog', 'blog__topic', 'blog__user')
        elif self.action in ('received'):
            queryset = queryset.filter(
                blog_id__gt=0,
                blog__user=self.request.user).select_related('blog', 'blog__topic', 'blog__user')
        else:
            queryset = queryset.select_related('user')
        return queryset

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """我的点赞
        """
        return super().list(request)

    @action(detail=False, methods=['get'])
    def received(self, request):
        """我收到的点赞
        """
        # 设置消息已读
        queryset = self.filter_queryset(self.get_queryset())
        queryset.filter(status=mm_Like.STATUS_CREATED).update(status=mm_Like.STATUS_READED)
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
