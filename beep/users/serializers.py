from rest_framework import serializers

from .models import User, CheckIn, Point, RelationShip, LableApply

base_user_fields = ['id',
                    'last_login',
                    'email',
                    'name',
                    'age',
                    'gender',
                    'avatar_url',
                    'create_at',
                    'update_at',
                    'desc',
                    'label_type',
                    ]
user_data_fields = [
    'total_blog',
    'total_following',
    'total_followers'
]
user_readonly_fields = [
    'last_login',
    'create_at',
    'update_at',
    'label_type',
]
user_import_info_fields = [
    'account',
    'date_joined',
]


class NoneSerializer(serializers.Serializer):
    pass


class AccountCheckSerializer(serializers.Serializer):

    account = serializers.CharField()

class RegisterSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField(max_length=4)
    invite_code = serializers.CharField(max_length=6, required=False)


class LoginSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField(required=False)
    code = serializers.CharField(max_length=4, required=False)


class MiniprogramLoginSerializer(serializers.Serializer):

    code = serializers.CharField()
    avatar_url = serializers.CharField()
    name = serializers.CharField(required=False, allow_blank=True)
    encryptedData = serializers.CharField()
    iv = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    is_following = serializers.SerializerMethodField(read_only=True)

    def get_is_following(self, obj):
        if 'request' not in self.context:
            return 0
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(user, '_following'):
            user._following = user.following_set.values_list('following_id', flat=True)
        return 1 if obj.id in user._following else 0

    class Meta:
        model = User
        fields = base_user_fields + ['is_following'] + user_data_fields
        read_only_fields = user_data_fields


class MyUserProfileSerializer(serializers.ModelSerializer):

    avatar_url_url = serializers.CharField(
        write_only=True, allow_blank=True, required=False)
    weixin_bind = serializers.SerializerMethodField()

    def get_weixin_bind(self, obj):
        return True if obj.openid else False

    class Meta:
        model = User
        fields = base_user_fields + ['avatar_url_url', 'is_superuser'] + user_data_fields + ['weixin_bind'] + user_import_info_fields + ['invite_code']
        read_only_fields = user_readonly_fields + user_data_fields + ['avatar_url', 'is_superuser', 'invite_code']


class ResetPasswordSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField()

class ResetPasswordSerializerV2(serializers.Serializer):

    raw_password = serializers.CharField()
    password = serializers.CharField()


class SendCodeSerializer(serializers.Serializer):

    code_type_choices = (
        ('enroll', '注册'),
        ('password', '重置密码'),
        ('login', '登陆'),
        ('bind_phone', '绑定手机'),
    )
    account = serializers.CharField(max_length=11)
    code_type = serializers.ChoiceField(
        choices=code_type_choices, default='enroll')



# ========= CheckIn Serializers  ==========

class CheckInSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckIn
        fields = ['id', 'create_at']

# ========= Point Serializers  ==========


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ['id', 'in_or_out', 'amount',
                  'total_left', 'action', 'desc', 'create_at', 'is_read']


class UserSampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'gender', 'avatar_url']


class UserBaseSerializer(serializers.ModelSerializer):

    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        if 'request' not in self.context:
            return 0
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(user, '_following'):
            user._following = user.following_set.values_list('following_id', flat=True)
        return 1 if obj.id in user._following else 0

    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'gender', 'avatar_url',  'label_type', 'desc', 'is_following']


class MyFollowingSerializer(serializers.ModelSerializer):

    following = UserBaseSerializer()

    class Meta:
        model = RelationShip
        fields = ['id', 'following', 'create_at']


class MyFollowersSerializer(serializers.ModelSerializer):

    user = UserBaseSerializer()

    class Meta:
        model = RelationShip
        fields = ['id', 'user', 'create_at']


class LabelApplySerializer(serializers.ModelSerializer):

    # DEFAULT_DATA = '{"total_view": 0, "total_followers": 0, "total_blog": 0}'

    # data_dict = serializers.JSONField(default=DEFAULT_DATA)

    class Meta:
        model = LableApply
        fields = ['id', 'lebel_type', 'image', 'desc',
                  'data_dict', 'status', 'create_at']
        read_only_fields = ['status']

