import traceback

from django.db import models
from django.db import transaction
from django.db import IntegrityError, DataError
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AuthUserManager


from utils.modelmanager import ModelManager

class UserManager(AuthUserManager, ModelManager):

    def add(self, account, password, **extra_fields):
        extra_fields.setdefault('account', account)
        return self.create_user(username=account, email=None, password=password, **extra_fields)


    def reset_password(self, account, password):
        """重置密码
        Arguments:
            cid {int} -- 用户id
        """
        user = self.filter(account=account).first()
        if user:
            user.set_password(password)
            user.save()



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
    mini_openid = models.CharField(max_length=40, unique=True, null=True, blank=True, verbose_name='小程序账号')
    name = models.CharField(max_length=30, blank=True, verbose_name='昵称')
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='年龄')
    gender = models.IntegerField(choices=GENDER_CHOICE, default=0, verbose_name='性别')
    avatar_url = models.CharField(max_length=300, blank=True, verbose_name='头像')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ['-id']
        verbose_name = verbose_name_plural = '用户信息'


mm_User = User.objects
