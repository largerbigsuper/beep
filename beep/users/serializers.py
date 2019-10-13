from rest_framework import serializers

from .models import User, Schedule, CheckIn, Point, RelationShip

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
                    ]
user_data_fields = [
    'total_blog',
    'total_following',
    'total_followers'
]


class NoneSerializer(serializers.Serializer):
    pass


class RegisterSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField(max_length=4)


class LoginSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField()


class MiniprogramLoginSerializer(serializers.Serializer):

    code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    is_following = serializers.SerializerMethodField(read_only=True)

    def get_is_following(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(user, '_following'):
            user._following = user.following_set.values_list(
                'following_id', flat=True)
        return 1 if obj.id in user._following else 0

    class Meta:
        model = User
        fields = base_user_fields + ['is_following'] + user_data_fields
        read_only_fields = user_data_fields


class MyUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class ResetPasswordSerializer(serializers.ModelSerializer):

    account = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField()

    class Meta:
        model = User
        fields = ['account', 'password', 'code']


# ========= Schedule Serializers  ==========

class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['id', 'plan_datetime', 'content', 'create_at']


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


class UserBaseSerializer(serializers.ModelSerializer):

    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(user, '_following'):
            user._following = user.following_set.values_list(
                'following_id', flat=True)
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


# =======================================
# ========= Admin Serializers  ==========
# =======================================
