from rest_framework import serializers

from .models import User, Schedule, CheckIn, Point


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

    class Meta:
        model = User
        fields = '__all__'


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
        fields = ['id', 'in_or_out', 'amount', 'total_left', 'action', 'desc', 'create_at']


# =======================================
# ========= Admin Serializers  ==========
# =======================================
