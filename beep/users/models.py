import random
import string
import traceback
from datetime import date

from django.db import models
from django.db import transaction
from django.db import IntegrityError, DataError
from django.db.models import F
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AuthUserManager
from django_extensions.db.fields.json import JSONField


from utils.exceptions import BeepException
from utils.modelmanager import ModelManager


class UserManager(AuthUserManager, ModelManager):

    Default_Password = '888888'
    
    LABEL_DEFAULT= 0
    LABEL_RED = 1
    LABEL_BLUE = 2
    LABEL_TYPE = (
        (LABEL_DEFAULT, '普通用户'),
        (LABEL_RED, '红V'),
        (LABEL_BLUE, '蓝V'),
    )

    def add(self, account, password, **extra_fields):
        extra_fields.setdefault('account', account)
        extra_fields.setdefault('name', account)
        return self.create_user(username=account, email=None, password=password, **extra_fields)

    def get_user_by_name(self, name):
        users = self.filter(name=name).values('id', 'name')
        if users:
            return users[0]
        else:
            return None

    def get_users(self, names_list=None):
        """通过name查找用户信息
        """
        users_list = []
        for name in names_list:
            info = self.get_user_by_name(name)
            if info:
                users_list.append(info)
        return users_list

    def get_info(self, user_id):
        """获取用户信息
        """
        cache_key = self.key_user_info.format(user_id)
        info = self.cache.get(cache_key)
        if not info:
            user = self.filter(pk=user_id).first()
            if user:
                info = {
                    'id': user_id,
                    'name': user.name,
                    'avatar_url': user.avatar_url_url,
                    'user_type': 'user'
                }
                self.cache.set(cache_key, info, self.TIME_OUT_USER_INFO)
            else:
                info = {}
        return info


    def _create_miniprogram_account(self, avatar_url, name, openid=None, mini_openid=None, unionid=None):
        account = 'bp_' + ''.join([random.choice(string.ascii_lowercase) for _ in range(8)])
        password = self.Default_Password
        name = 'bp' + account[-2:] + '_' + name
        user = self.add(account, password, mini_openid=mini_openid, openid=openid, unionid=unionid, avatar_url=avatar_url, name=name)
        return user

    def get_user_by_miniprogram(self, avatar_url, name, openid=None, mini_openid=None, unionid=None):
        """通过小程序获取User
        前期有小程序登陆用户，但是没有unionid， 需要同步小程序应用与微信网页应用
        """
        user = None
        if unionid:
            user = self.filter(unionid=unionid).first()
            if user:
                if mini_openid:
                    user.mini_openid = mini_openid
                if openid:
                    user.openid = openid
                user.save()
                return user

        if mini_openid:
            user = self.filter(mini_openid=mini_openid).first()
        if openid:
            user = self.filter(openid=openid).first()
            
        if user:
            user.unionid = unionid
            if mini_openid:
                user.mini_openid = mini_openid
            if openid:
                user.openid = openid
            user.save()
            return user
        else:
            user = self._create_miniprogram_account(avatar_url, name, openid, mini_openid, unionid)
            if user:
                return user
            else:
                raise IntegrityError('注册用户失败')

    def get_user_by_unionid(self, unionid):
        """通过unionid获取用户，忽略小程序未绑定主体的用户
        """
        user = self.filter(unionid=unionid).first()
        return user

    def get_by_account(self, account):
        user = self.filter(account=account).first()
        return user


    def reset_password(self, account, password):
        """重置密码
        Arguments:
            cid {int} -- 用户id
        """
        user = self.filter(account=account).first()
        if user:
            user.set_password(password)
            user.save()
        else:
            raise BeepException('账号不存在')

    def update_data(self, pk, field_name, amount=1):
        if amount > 0: 
            value = F(field_name) + amount
        else:
            value = F(field_name) - abs(amount)
        updates = {
            field_name: value
        }
        self.filter(pk=pk).update(**updates)

    def get_obj_by_name(self, name):
        return self.filter(name=name).first()

class User(AbstractUser):
    GENDER_UNSET = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICE = (
        (GENDER_UNSET, '未知'),
        (GENDER_MALE, '男'),
        (GENDER_FEMALE, '女'),
    )

    account = models.CharField(max_length=40, unique=True, verbose_name='账号')
    mini_openid = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name='小程序账号')
    openid = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name='微信账号')
    unionid = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name='微信unionid')
    name = models.CharField(max_length=30, blank=True, unique=True, verbose_name='昵称')
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='年龄')
    gender = models.IntegerField(choices=GENDER_CHOICE, default=0, verbose_name='性别')
    avatar_url = models.ImageField(blank=True, default='', verbose_name='头像')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    desc = models.CharField(max_length=500, blank=True, null=True, verbose_name='个人简介')
    total_blog = models.PositiveIntegerField(default=0, verbose_name='博文数量')
    total_following = models.PositiveIntegerField(default=0, verbose_name='关注数量')
    total_followers = models.PositiveIntegerField(default=0, verbose_name='粉丝数量')
    label_type = models.PositiveIntegerField(choices=UserManager.LABEL_TYPE, default=UserManager.LABEL_DEFAULT, verbose_name='普通用户|红V|蓝V')

    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ['-id']
        verbose_name = verbose_name_plural = '用户信息'

    def __str__(self):
        return self.account

    @property
    def avatar_url_url(self):
        if self.avatar_url:
            return self.avatar_url.url
        else:
            return ''


mm_User = User.objects


class PointManager(ModelManager):
    POINT_OUT = 0
    POINT_IN = 1
    POINT_OP_CHOICE = (
        (POINT_OUT, '减少'),
        (POINT_IN, '增加'),
    )

    ACTION_CHECK_IN = 0
    ACTION_SKU_EXCHANGE_PAY = 1
    ACTION_SKU_EXCHANGE_REFOUND = 2

    ACTION_CHOICE = (
        (ACTION_CHECK_IN, '每日签到'),
        (ACTION_SKU_EXCHANGE_PAY, '兑换商品消费'),
        (ACTION_SKU_EXCHANGE_REFOUND, '兑换商品退回'),
    )
    ACTION_IN_OR_OUT_MAPPING = {
        ACTION_CHECK_IN: POINT_IN,
        ACTION_SKU_EXCHANGE_PAY: POINT_OUT,
        ACTION_SKU_EXCHANGE_REFOUND: POINT_IN,

    }

    Action_Point_Mapping = {
        ACTION_CHECK_IN: 30,
    }

    Action_Desc = {action: msg for action, msg in ACTION_CHOICE}

    def get_total_point(self, user_id):
        record = self.filter(user_id=user_id).first()
        if record:
            return record.total_left
        else:
            return 0

    def _add_action(self, user_id, action, amount, total_left, operator_id=None):
        """
        积分记录
        :param customer_id: 用户id
        :param amount: 操作总量
        :param action: 行为
        :param operator_id: 操作人auth_user.id
        :return:
        """
        in_or_out = self.ACTION_IN_OR_OUT_MAPPING[action]
        self.create(user_id=user_id,
                    in_or_out=in_or_out,
                    amount=amount,
                    total_left=total_left,
                    action=action,
                    desc=self.Action_Desc[action],
                    operator_id=operator_id,
                    )

    def add_action(self, user_id, action, amount=None):
        """
        增加积分记录
        :param customer_id:
        :param action:
        :return:
        """
        if amount is None:
            amount = self.Action_Point_Mapping[action]
        if self.ACTION_IN_OR_OUT_MAPPING[action]:
            total_left = self.get_total_point(user_id) + amount
        else:
            total_left = self.get_total_point(user_id) - amount
        self._add_action(user_id=user_id,
                         action=action,
                         amount=amount,
                         total_left=total_left,
                         )


class Point(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='points',
                             verbose_name='用户')
    in_or_out = models.PositiveSmallIntegerField(choices=PointManager.POINT_OP_CHOICE,
                                                 default=PointManager.POINT_IN,
                                                 verbose_name='增加|减少')
    amount = models.PositiveSmallIntegerField(default=0, verbose_name='数量')
    total_left = models.PositiveIntegerField(default=0, verbose_name='剩余数量')
    action = models.PositiveSmallIntegerField(
        choices=PointManager.ACTION_CHOICE, default=0, verbose_name='原因')
    desc = models.CharField(verbose_name='描述', max_length=48)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True, verbose_name='操作人')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    objects = PointManager()

    class Meta:
        db_table = 'user_points'
        ordering = ['-create_at']
        verbose_name = '用户积分'
        verbose_name_plural = '用户积分'


mm_Point = Point.objects


class CheckInManager(ModelManager):

    def is_check_in(self, user_id):
        return self.filter(user_id=user_id, create_at__gt=date.today()).exists()


class CheckIn(models.Model):
    """用户签到表
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='用户')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    objects = CheckInManager()

    class Meta:
        db_table = 'user_checkin'
        ordering = ['-create_at']


mm_CheckIn = CheckIn.objects


class RelationShipManager(ModelManager):

    def add_relation(self, user, following):
        """添加关注
        """
        created, relation = self.get_or_create(user=user, following=following)
        return relation

    def remove_relation(self, user, following):
        """取消关注
        """
        self.filter(user=user, following=following).delete()


class RelationShip(models.Model):
    """用户关系"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='following_set', verbose_name='我')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='followers_set', verbose_name='关注的人')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = RelationShipManager()

    class Meta:
        db_table = 'user_relationship'
        index_together = [
            ['user', 'following']
        ]
        unique_together = [
            ['user', 'following']
        ]


mm_RelationShip = RelationShip.objects


class LableApplyManager(ModelManager):
    
    STATUS_SUBMITED = 0
    STATUS_PASSED = 1
    STATUS_FAILED = 2
    STATUS_CHOICE = (
        (STATUS_SUBMITED, '已提交'),
        (STATUS_PASSED, '审核通过'),
        (STATUS_FAILED, '审核失败'),
    )
    
    DEFAULT_DATA = '{"total_view": 0, "total_followers": 0, "total_blog": 0}'

class LableApply(models.Model):
    """标签申请记录"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='用户')
    lebel_type = models.PositiveSmallIntegerField(choices=UserManager.LABEL_TYPE,
                                                  default=UserManager.LABEL_RED,
                                                  verbose_name='红V|蓝V')
    image = models.CharField(max_length=200, blank=True, null=True, verbose_name='证件照')
    desc = models.CharField(max_length=500, blank=True, null=True, verbose_name='描述')
    data_dict = JSONField(default=LableApplyManager.DEFAULT_DATA, verbose_name='数据信息')
    status = models.PositiveSmallIntegerField(choices=LableApplyManager.STATUS_CHOICE,
                                                  default=LableApplyManager.STATUS_SUBMITED,
                                                  verbose_name='审核状态')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = LableApplyManager()

    class Meta:
        db_table = 'label_apply'
        ordering = ['-create_at']
        verbose_name = verbose_name_plural = '加V申请'

mm_LableApply = LableApply.objects

