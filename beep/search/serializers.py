from rest_framework import serializers

from .models import SearchHistory, SearchKeyWord

class SearchHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchHistory
        fields = ('id', 'content')

    def create(self, validated_data):
        user = self.context['request'].user
        instance = self.Meta.model(user=user, **validated_data)
        instance.save()
        return instance


class SearchKeyWordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchKeyWord
        fields = ('keyword')