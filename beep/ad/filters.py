from django_filters import rest_framework as filters

from .models import Ad

class AdFilter(filters.FilterSet):

    class Meta:
        model = Ad
        fields = {
            'ad_type': ['exact'],
            'module_type': ['exact'],
            'position_type': ['exact'],
        }