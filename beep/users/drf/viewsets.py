import requests
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, MiniprogramLoginSerializer, MyUserProfileSerializer, ResetPasswordSerializer
from utils.common import process_login, process_logout
from utils.qiniucloud import QiniuService
from beep.users.models import mm_User


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = []
    serializer_class = UserSerializer
    queryset = mm_User.all()
    

    @action(detail=False, methods=['post'], serializer_class=RegisterSerializer)
    def enroll(self, request):
        """注册"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        password = serializer.validated_data['password']
        # code = serializer.validated_data['code']
        user = mm_User.add(account=account, password=password)
        return Response(data={'account': account})

    @action(detail=False, methods=['post'], serializer_class=MiniprogramLoginSerializer, permission_classes=[], authentication_classes=[])
    def login_miniprogram(self, request):
        """小程序登录
        1. csrf校验去除
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        wx_res = requests.get(settings.MinprogramSettings.LOGIN_URL + code)
        ret_json = wx_res.json()
        if 'openid' not in ret_json:
            return Response(data=ret_json, status=status.HTTP_400_BAD_REQUEST)
        openid = ret_json['openid']
        # session_key = ret_json['session_key']
        # unionid = ret_json.get('session_key')
        user = mm_User.get_customer_by_miniprogram(openid)
        process_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'id': user.id,
            'name': user.name,
            'token': token.key,
        }
        return Response(data=data)

    @action(detail=False, methods=['post'], serializer_class=LoginSerializer, permission_classes=[], authentication_classes=[])
    def login(self, request):
        """登录"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        password = serializer.validated_data['password']
        user = mm_User.filter(account=account).first()
        if user:
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

    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """个人信息获取／修改"""
        
        if request.method == 'GET':
            serializer = self.serializer_class(request.user)
            return Response(data=serializer.data)
        else:
            serializer = self.serializer_class(request.user, data=request.data, partial=True)
            if serializer.is_valid():
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
        if _code == code:
            mm_User.reset_password(account, password)
            return Response()
        else:
            data = {
                'detail': '验证码错误'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated,])
    def qiniutoken(self, request):
        """获取七牛token
        """
        file_type = request.query_params.get('file_type', 'image')
        bucket_name = QiniuService.get_bucket_name(file_type)
        token = QiniuService.gen_app_upload_token(bucket_name)
        data = {'token': token}
        return Response(data=data)
