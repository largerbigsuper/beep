from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .serializers import (ActivityCreateSerializer, ActivityListSerializer,
                          RegistrationCreateSerializer, RegistrationListSerializer,
                          CollectCreateSerializer, CollectListSerializer, MyCollectListSerializer,
                          RewardPlanApplyCreateSerializer, RewardPlanApplySerializer, RewardPlanApplyListSerializer,
                          RewardPlanSerializer, RewardPlanCreateSerializer, ScheduleSerializer,
                          )
from .models import mm_Activity, mm_Registration, mm_Collect, mm_RewardPlan, mm_RewardPlanApply, mm_Schedule
from .filters import ActivityFilter, CollectFilter, RewardPlanApplyFilter, RegistrationFilter, ScheduleFilter
from .tasks import send_rewardplan_start, generate_activity_poster

from beep.blog.models import mm_Blog
from utils.permissions import IsOwerPermission, IsOwnerOrAdminPermission
from utils.pagination import Size_200_Pagination, Size_12_Pagination
from utils.wexin_api import WeiXinOpenApi
from utils.serializers import NoneParamsSerializer
from utils.post.gen_poster import Post

class ActivityViewSet(viewsets.ModelViewSet):


    queryset = mm_Activity.valid().select_related('user', 'rewardplan')
    filter_class = ActivityFilter
    pagination_class = Size_12_Pagination

    def get_permissions(self):
        if self.action in ['create', 'put', 'delete']:
            return [IsAuthenticated()]
        elif self.action in ['set_live_start', 'set_live_end']:
            return [IsOwnerOrAdminPermission()]
        else:
            return []

    def get_serializer_class(self):
        if self.action in ['create', 'put']:
            return ActivityCreateSerializer
        elif self.action in ['remove_registration', 'remove_collect', 'delete', 'set_live_start', 'set_live_end']:
            return NoneParamsSerializer
        else:
            return ActivityListSerializer            

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.is_valid(raise_exception=True)
            # 微信内容校验
            WeiXinOpenApi().check_content(serializer.validated_data)

            # rewardplan
            rewardplan_dict = serializer.validated_data.pop('rewardplan', None)
            if rewardplan_dict:
                coin_logo = rewardplan_dict.pop('coin_logo_url', None)
                serializer_rewardplan = RewardPlanCreateSerializer(data=rewardplan_dict)
                serializer_rewardplan.is_valid()
                serializer_rewardplan.validated_data['coin_logo'] = coin_logo
                rewardplan = serializer_rewardplan.save()
            else:
                rewardplan = None
            cover_url = serializer.validated_data.pop('cover_url', None)
            serializer.validated_data['cover'] = cover_url
            activity = serializer.save(user=self.request.user, rewardplan=rewardplan)
            # 生成海报
            generate_activity_poster.delay(activity.id)

    def perform_update(self, serializer):
        # 生成海报
        activity = serializer.save()
        generate_activity_poster.delay(activity.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        mm_Activity.update_data(instance.id, 'total_view')
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_registration(self, request, pk=None):
        """取消报名
        """
        activity = self.get_object()
        record = mm_Registration.filter(user=request.user, activity=activity).first()
        if record:
            record.delete()
            mm_Activity.update_data(activity.id, 'total_registration', -1)
            mm_Schedule.remove_activity(user_id=request.user.id, activity=activity, add_type='registration')
        return Response()

    @action(detail=True, methods=['post'])
    def remove_collect(self, request, pk=None):
        """取消收藏
        """
        activity = self.get_object()
        record = mm_Collect.filter(user=request.user, activity=activity).first()
        if record:
            record.delete()
            mm_Activity.update_data(activity.id, 'total_collect', -1)
            mm_Schedule.remove_activity(user_id=request.user.id, activity=activity, add_type='collect')
        return Response()

    @action(detail=True, methods=['get'])
    def get_question_status(self, request, pk=None):
        """获取提问状态
        """
        obj = self.get_object()
        data = {
            'ask_allowed': obj.ask_allowed
        }
        return Response(data=data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_rewardplan_result(self, request, pk=None):
        """获取抽奖结果【定时任务会触发产生结果】
        """
        
        activity = self.get_object()
        data = []
        if activity.rewardplan:
            data = activity.rewardplan.result
        return Response(data=data)

    @action(detail=True, methods=['get'])
    def get_rewardplan_detail(self, request, pk=None):
        """获取空投详情
        """
        activity = self.get_object()
        if activity.rewardplan:
            applys_qs = mm_RewardPlanApply.filter(rewardplan=activity.rewardplan)
            applyer_serializer = RewardPlanApplyListSerializer(applys_qs, many=True)
            rewardplan_serizlizer = RewardPlanSerializer(activity.rewardplan, context={'request': request})
            data = rewardplan_serizlizer.data
            data['applyers'] = applyer_serializer.data
        else:
            data = {}
        return Response(data=data)

    @action(detail=False, methods=['get'])
    def recommand_list(self, request):
        """活动推荐
        """
        queryset = mm_Activity.recommand()[:5]
        serializer = ActivityListSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data)


    @action(detail=True, methods=['post'])
    def set_live_start(self, request, pk=None):
        """设置活动直播开始
        """
        activity = self.get_object()
        if activity.wx_groupwxid:
            live_rooms = mm_Activity.cache.get(mm_Activity.key_live_rooms, set())
            live_rooms.add(activity.wx_groupwxid)
            mm_Activity.cache.set(mm_Activity.key_live_rooms, live_rooms, 60*60*24*3)

        return Response()


    @action(detail=True, methods=['post'])
    def set_live_end(self, request, pk=None):
        """设置活动直播结束
        """
        activity = self.get_object()
        if activity.wx_groupwxid:
            live_rooms = mm_Activity.cache.get(mm_Activity.key_live_rooms, set())
            live_rooms.remove(activity.wx_groupwxid)
            mm_Activity.cache.set(mm_Activity.key_live_rooms, live_rooms, 60*60*24*3)

        return Response()

    @action(detail=True, methods=['get'])
    def get_live_status(self, request, pk=None):
        """获取活动直播状态
        """
        activity = self.get_object()
        live = False
        if activity.wx_groupwxid:
            live_rooms = mm_Activity.cache.get(mm_Activity.key_live_rooms, set())
            if activity.wx_groupwxid in live_rooms:
                live = True
        data = {
            'live': live
        }
        return Response(data=data)

    # @action(detail=True, methods=['post'])
    # def create_poster(self, request, pk=None):
    #     """生成海报
    #     """
    #     activity = self.get_object()
    #     user_cover = activity.user.avatar_url
    #     user_name = activity.user.name
    #     user_desc = activity.user.desc[:30] if activity.user.desc else ''
    #     title = activity.title
    #     logo = activity.cover
    #     qrcode_path = 'https://beepcrypto.com/activity/detail?id={}&articleId={}'.format(activity.id, activity.blog_id)

    #     detail = ''
    #     if not user_cover:
    #         detail = '用户头像未设置'
    #     if not logo:
    #         detail = '活动封面图未设置'
    #     if detail:
    #         return Response(data={'detail': detail}, status=status.HTTP_400_BAD_REQUEST)
        
    #     poster = Post().generate_post_activity(user_cover, user_name, user_desc, title, logo, qrcode_path)
    #     mm_Activity.filter(pk=activity.id).update(poster=poster)
    #     data = {
    #         'poster': poster
    #     }
    #     return Response(data)

    @action(detail=True)
    def get_poster(self, request, pk=None):
        """获取海报
        """
        obj = self.get_object()
        data = {
            'poster': obj.poster.url if obj.poster else ''
        }
        return Response(data)

class RegistrationViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    """报名

    create -- 报名
    list -- 我的报名列表
    destory -- 删除报名
    """
    filter_class = RegistrationFilter
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
        mm_Schedule.add_activity(user_id=self.request.user.id, activity=instance.activity, add_type='registration')
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
        mm_Schedule.add_activity(user_id=self.request.user.id, activity=instance.activity, add_type='registration')
    
    def perform_destroy(self, instance):
        # 更新收藏统计
        mm_Activity.update_data(instance.activity_id, 'total_collect', -1)
        instance.delete()

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """我的收藏列表
        """

        return super().list(request)


class RewardPlanApplyViewSet(viewsets.ModelViewSet):
    """空投报名
    mine -- 我的报名记录
    list -- 列表
    """

    permission_class = [IsAuthenticated,]
    filter_class = RewardPlanApplyFilter
    pagination_class = Size_200_Pagination
    queryset = mm_RewardPlanApply.all()
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return RewardPlanApplyCreateSerializer
        else:
            return RewardPlanApplySerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        rewardplan = serializer.validated_data['rewardplan']
        serializer.save(user=self.request.user, activity=rewardplan.activity)

    @action(detail=False)
    def mine(self, request):
        """我的提交记录
        """
        self.queryset = mm_RewardPlanApply.filter(user=request.user)
        return super().list(request)


class RewardPlanViewSet(viewsets.ModelViewSet):
    """空投api
    """
    permission_class = []
    serializer_class = RewardPlanSerializer
    queryset = mm_RewardPlan.all()


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def set_rewardplan_start(self, request, pk=None):
        """发送开奖信息到频道
        """ 
        # obj = self.get_object()
        send_rewardplan_start(int(pk))
        return Response()


class ScheduleViewSet(viewsets.ModelViewSet):
    """用户行程表
    """
    
    filter_class = ScheduleFilter
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return mm_Schedule.filter(user=self.request.user)

    def perform_create(self, serailizer):
        serailizer.save(user=self.request.user)

