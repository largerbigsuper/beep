from rest_framework import serializers

from .models import News

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'origin', 'update_at', 'published_at')


class AdminNewsSerialzier(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = '__all__'
        