from rest_framework import serializers

from .models import ActionPointCfg


class ActionPointCfgSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionPointCfg
        fields = ('id', 'code', 'name', 'point', 'max_per_day', 'is_on')