from rest_framework import serializers

from beep.users.models import User


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

# =======================================
# ========= Admin Serializers  ==========
# =======================================