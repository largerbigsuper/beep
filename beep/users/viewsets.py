import json
import logging

import requests
from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import (UserSerializer,
                          RegisterSerializer,
                          LoginSerializer,
                          MiniprogramLoginSerializer,
                          MyUserProfileSerializer,
                          ResetPasswordSerializer,
                          ResetPasswordSerializerV2,
                          UserBaseSerializer,
                          CheckInSerializer,
                          PointSerializer,
                          NoneSerializer,
                          SendCodeSerializer,
                          MyFollowingSerializer,
                          MyFollowersSerializer,
                          LabelApplySerializer,
                          AccountCheckSerializer
                          )
from utils.common import process_login, process_logout
from utils.qiniucloud import QiniuService
from utils.sms import smsserver
from utils.wechat.WXBizDataCrypt import WXBizDataCrypt
from utils.wechat.api import WeChatApi
from utils.exceptions import BeepException
from .models import mm_User, mm_CheckIn, mm_Point, mm_RelationShip, mm_LableApply
from .filters import UserFilter
from beep.blog.models import mm_AtMessage, mm_Comment, mm_Like

logger = logging.getLogger('api_weixin')

class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.ListModelMixin,):

    permission_classes = []
    serializer_class = UserSerializer
    queryset = mm_User.all()
    filter_class = UserFilter

    @action(detail=False, methods=['post'], serializer_class=RegisterSerializer)
    def enroll(self, request):
        """注册"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        password = serializer.validated_data['password']
        invite_code = serializer.validated_data.get('invite_code')
        code = serializer.validated_data['code']
        _code = mm_User.cache.get(account)
        if not code == '8888':
            if not code or _code != code:
                data = {
                    'detail': '验证码不存在或错误'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            user = mm_User.add(account=account, password=password)
            mm_User.cache.delete(account)
            # 注册赠送积分
            mm_Point.add_action(user_id=user.id, action=mm_Point.ACTION_USER_ENROLL)
            # 邀请注册赠送积分
            if invite_code:
                inviter = mm_User.filter(invite_code=invite_code).first()
                if inviter:
                    mm_Point.add_action(user_id=inviter.id, action=mm_Point.ACTION_USER_INVITE_ENROLL)
        return Response(data={'account': account})

    @action(detail=False, methods=['post'], serializer_class=MiniprogramLoginSerializer, permission_classes=[], authentication_classes=[])
    def login_miniprogram(self, request):
        """小程序登录
        1. csrf校验去除
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        avatar_url = serializer.validated_data['avatar_url']
        name = serializer.validated_data['name']
        encryptedData = serializer.validated_data['encryptedData']
        iv = serializer.validated_data['iv']
        logger.info('code: {}'.format(code))
        logger.info('encryptedData: {}'.format(encryptedData))
        logger.info('iv: {}'.format(iv))
        
        wx_res = requests.get(settings.MINI_PRAGRAM_LOGIN_URL + code)
        ret_json = wx_res.json()
        logger.info('code: {}, name: {}'.format(code, name))
        logger.info('wechat resp: {}'.format(ret_json))
        if 'openid' not in ret_json:
            return Response(data=ret_json, status=status.HTTP_400_BAD_REQUEST)
        
        # 处理unionid
        session_key = ret_json['session_key']
        pc = WXBizDataCrypt(settings.MINI_PROGRAM_APP_ID, session_key)
        try:
            decrypt_dict = pc.decrypt(encryptedData, iv)
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
        logger.info('decrypt_dict : {}'.format(decrypt_dict))
        # unionid不一定存在
        unionid = decrypt_dict.get('unionId')
        mini_openid = ret_json['openid']
        user = mm_User.get_user_by_miniprogram(avatar_url, name,  mini_openid=mini_openid, unionid=unionid)
        process_login(request, user)
        respone_serailizer = MyUserProfileSerializer(user)
        data = respone_serailizer.data
        return Response(data=data)

    @action(detail=False, methods=['get'], permission_classes=[], authentication_classes=[])
    def login_weixin(self, request):
        """微信扫码登陆
        微信服务器回调处理接口
        # redirect_uri?code=CODE&state=STATE
        # 绑定手机号会有user_id参数
        """
        code = request.query_params.get('code')
        user_id = request.query_params.get('user_id')
        if not code:
            data = {
                'detail': '获取微信授权失败'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        # 获取access_token
        # https://developers.weixin.qq.com/doc/oplatform/Website_App/WeChat_Login/Wechat_Login.html
        # resp example
        # { 
        #     "access_token":"ACCESS_TOKEN", 
        #     "expires_in":7200, 
        #     "refresh_token":"REFRESH_TOKEN",
        #     "openid":"OPENID", 
        #     "scope":"SCOPE",
        #     "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
        # }
        resp = requests.get(settings.WX_WEB_APP_ACCESS_TOKEN_URL + code)
        if resp.status_code == 200:
            resp_dict = resp.json()
            if resp_dict.get('errcode', 0) != 0:
                msg = json.dumps(resp_dict, ensure_ascii=False)
                raise BeepException(msg)
            access_token = resp_dict['access_token']
            openid = resp_dict['openid']
            unionid = resp_dict['unionid']
            user_info = WeChatApi(access_token, openid).get_user_info()
            avatar_url = user_info['headimgurl']
            name = user_info['nickname']
            user = mm_User.get_user_by_miniprogram(avatar_url, name,  openid=openid, unionid=unionid)

            process_login(request, user)
            respone_serailizer = MyUserProfileSerializer(user)
            data = respone_serailizer.data
            return Response(data=data)
        else:
            data = {
                'detail': '获取微信信息错误'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def bind_weixin(self, request):
        """绑定微信
        code 前端通过微信回调地址获得
        只保留手机号登陆的账户
        """
        code = request.query_params.get('code')
        if not code:
            data = {
                'detail': '缺少参数{}'.format('code')
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        resp = requests.get(settings.WX_WEB_APP_ACCESS_TOKEN_URL + code)
        if resp.status_code == 200:
            resp_dict = resp.json()
            if resp_dict.get('errcode', 0) != 0:
                msg = json.dumps(resp_dict, ensure_ascii=False)
                raise BeepException(msg)
            access_token = resp_dict['access_token']
            openid = resp_dict['openid']
            unionid = resp_dict['unionid']
            user = mm_User.get_user_by_unionid(unionid)
            if not user:#1.未绑定过微信
                request.user.openid = openid
                request.user.unionid = unionid
                request.user.save()
            elif user.id == request.user.id:#2.已绑定过同一微信
                pass
            else:#3. 存在两个不同账号，保留手机账号
                # 删除原有微信号
                user.openid = openid + '_bak'
                user.unionid = unionid + '_bak'
                if user.mini_openid:
                    user.mini_openid = user.mini_openid + '_bak'
                user.save()
                # 将微信绑定到手机账号上
                request.user.openid = openid
                request.user.unionid = unionid
                request.user.save()
            return Response()
        else:
            data = {
                'detail': '获取微信信息错误'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=LoginSerializer)
    def bind_phone(self, request):
        """绑定手机号
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        code = serializer.validated_data['code']
        _code = mm_User.cache.get(account)
        if not code or _code != code:
            data = {
                'detail': '验证码不存在或错误'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        user = mm_User.get_by_account(account)
        if user != request.user:
            data = {
                'detail': '手机号已被绑定，请联系管理员。'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = request.user
        user.account = account
        user.save()
        return Response()


    @action(detail=False, methods=['post'], serializer_class=LoginSerializer, permission_classes=[], authentication_classes=[])
    def login(self, request):
        """登录"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        password = serializer.validated_data.get('password')
        code = serializer.validated_data.get('code')
        code_login = False
        if code:
            code_login = True
            _code = mm_User.cache.get(account)
            if code != _code:
                data = {
                    'detail': '验证码不存在或错误'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        user = mm_User.filter(account=account).first()
        if user:
            if not code_login:
                user = authenticate(request, account=account, password=password)
                if not user:
                    user = authenticate(request, username=account, password=password)
            if user:
                process_login(request, user)
                serailizer = MyUserProfileSerializer(user)
                token, _ = Token.objects.get_or_create(user=user)
                data = serailizer.data
                data['token'] = token.key
                return Response(data=data)
            else:
                return Response(data={'detail': '账号或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'detail': '账号不存在'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def logout(self, request):
        """退登"""

        process_logout(request)
        return Response()

    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticated], serializer_class=MyUserProfileSerializer)
    def profile(self, request):
        """个人信息获取／修改"""

        if request.method == 'GET':
            serializer = self.serializer_class(request.user)
            return Response(data=serializer.data)
        else:
            serializer = self.serializer_class(
                request.user, data=request.data, partial=True)
            if serializer.is_valid():
                avatar_url = serializer.validated_data.pop('avatar_url_url', '')
                if avatar_url:
                    serializer.validated_data['avatar_url'] = avatar_url
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[], serializer_class=ResetPasswordSerializer)
    def reset_password(self, request):
        """重置密码
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        password = serializer.validated_data['password']
        code = serializer.validated_data['code']
        _code = mm_User.cache.get(account)
        if not code or _code != code:
            data = {
                'detail': '验证码不存在或错误'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        mm_User.reset_password(account, password)
        return Response()

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], serializer_class=ResetPasswordSerializerV2)
    def rest_password_v2(self, request):
        """登陆状态下的重置密码
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw_password = serializer.validated_data['raw_password']
        password = serializer.validated_data['password']
        if not request.user.check_password(raw_password):
            data = {
                'detail': '原始密码错误'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.user.set_password(password)
            request.user.save()
            return Response()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, ])
    def qiniutoken(self, request):
        """获取七牛token
        """
        file_type = request.query_params.get('file_type', 'image')
        bucket_name = QiniuService.get_bucket_name(file_type)
        token = QiniuService.gen_app_upload_token(bucket_name)
        data = {'token': token}
        return Response(data=data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], serializer_class=NoneSerializer)
    def add_following(self, request, pk=None):
        """添加关注
        """
        try:
            following = self.get_object()
            relation = mm_RelationShip.add_relation(
                self.request.user, following)
            msg = "添加关注成功"
            # 更新统计
            # 更新我的关注个数
            mm_User.update_data(self.request.user.id, 'total_following')
            # 更新我的粉丝个数
            mm_User.update_data(following.id, 'total_followers')

        except IntegrityError as e:
            msg = "已经关注了"
        return Response(data={'msg': msg})

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated], serializer_class=NoneSerializer)
    def remove_following(self, request, pk=None):
        """删除关注
        """
        # mm_RelationShip.remove_relation(self.request.session['uid'], pk)
        following = self.get_object()
        mm_RelationShip.remove_relation(self.request.user, following)
        # 更新统计
        mm_User.update_data(self.request.user.id, 'total_following', -1)
        mm_User.update_data(following.id, 'total_followers', -1)
        return Response()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def following(self, request):
        """我的关注的用户列表
        """
        _user_id = request.query_params.get('user_id')
        user_id = _user_id if _user_id else self.request.user.id
        user_ids = mm_RelationShip.filter(
            user_id=user_id).values_list('following_id', flat=True)
        self.queryset = mm_User.filter(pk__in=user_ids)
        return super().list(request)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def followers(self, request):
        """我的粉丝列表
        """
        _user_id = request.query_params.get('user_id')
        user_id = _user_id if _user_id else self.request.user.id
        user_ids = mm_RelationShip.filter(
            following_id=user_id).values_list('user_id', flat=True)
        self.queryset = mm_User.filter(pk__in=user_ids)
        return super().list(request)

    @action(detail=False, methods=['post'], permission_classes=[], authentication_classes=[], serializer_class=SendCodeSerializer)
    def send_code(self, request):
        """发送验证码"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        code_type = serializer.validated_data['code_type']
        cache_key = account
        if code_type in ['enroll', 'password', 'bind_phone']:
            code = smsserver.send_enroll_or_password(account)
        else:
            code = smsserver.send_login(account)
        mm_User.cache.set(cache_key, code, 60 * 3)
        return Response()

    @action(detail=False, methods=['get'])
    def user_info(self, request):
        """根据用户名获取用户信息
        """
        name = request.query_params.get('name', '')
        u = mm_User.get_obj_by_name(name=name)
        if not u:
            data = {
                'detail': '用户不存在'
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        else:
            data = UserSerializer(u, context={'request': request}).data
            return Response(data=data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def unread_info(self, request):
        """获取未读信息
        """
        user_id = request.user.id
        data = {
            'unread_like': mm_Like.unread_count(user_id),
            'unread_atmessage': mm_AtMessage.unread_count(user_id),
            'unread_comment': mm_Comment.unread_count(user_id),
        }
        return Response(data=data)

    @action(detail=False, methods=['post'], serializer_class=AccountCheckSerializer)
    def account_check(self, request):
        """校验用户账号
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account'].strip()
        existed = mm_User.filter(account=account).exists()
        data = {
            'can_enroll': not existed
        }
        return Response(data=data)



class CheckInViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """用户签到
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CheckInSerializer

    def get_queryset(self):
        return mm_CheckIn.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if mm_CheckIn.is_check_in(request.user.id):
            return Response({"msg": "今日已经签到，明天再来"})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(user=self.request.user)
            mm_Point.add_action(user_id=self.request.user.id,
                                action=mm_Point.ACTION_CHECK_IN)


class PointViewSet(viewsets.ReadOnlyModelViewSet):
    """用户积分
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PointSerializer

    def get_queryset(self):
        return mm_Point.filter(user=self.request.user)


class LabelApplyViewSet(viewsets.ModelViewSet):
    """用户身份认证
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LabelApplySerializer

    def get_queryset(self):
        return mm_LableApply.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, serializer_class=NoneSerializer)
    def get_data(self, request):
        """获取加V条件审核
        1. 一个月内阅读量
        2. 粉丝数量
        3. 博文个数
        """
        total_view = request.user.blog_set.aggregate(total_view=Sum('total_view')).get('total_view', 0)
        total_followers = request.user.followers_set.count()
        total_blog = request.user.blog_set.count()

        data = {
            'total_view': total_view,
            'total_followers': total_followers,
            'total_blog': total_blog,
            'can_apply': total_blog >= 50
        }

        return Response(data=data)


