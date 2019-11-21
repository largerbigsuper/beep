from rest_framework import serializers

from .models import User, CheckIn, Point, RelationShip, LableApply

base_user_fields = ['id',
                    'last_login',
                    'is_superuser',
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'is_staff',
                    'is_active',
                    'date_joined',
                    'account',
                    'mini_openid',
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
    'username',
    'account',
    'last_login',
    'is_superuser',
    'first_name',
    'last_name',
    'is_staff',
    'is_active',
    'date_joined',
    'mini_openid',
    'create_at',
    'update_at',
    'label_type',
]


class NoneSerializer(serializers.Serializer):
    pass


class RegisterSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField(max_length=4)


class LoginSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField(required=False)
    code = serializers.CharField(max_length=4, required=False)


class MiniprogramLoginSerializer(serializers.Serializer):

    code = serializers.CharField()
    avatar_url = serializers.CharField()
    name = serializers.CharField()


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

    class Meta:
        model = User
        fields = base_user_fields + ['avatar_url_url'] + user_data_fields
        read_only_fields = user_readonly_fields + user_data_fields + ['avatar_url']


class ResetPasswordSerializer(serializers.ModelSerializer):

    account = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField()

    class Meta:
        model = User
        fields = ['account', 'password', 'code']


class SendCodeSerializer(serializers.Serializer):

    code_type_choices = (
        ('enroll', '注册'),
        ('password', '重置密码'),
        ('login', '登陆'),
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
                  'total_left', 'action', 'desc', 'create_at']


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
        fields = ['id', 'name', 'age', 'gender', 'avatar_url', 'is_following']


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


# =======================================
# ========= Admin Serializers  ==========
# =======================================
