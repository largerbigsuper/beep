from django_filters import rest_framework as filters

from .models import Sku

class SkuFilter(filters.FilterSet):

    class Meta:
        model = Sku
        fields = {
            'name': ['contains'],
        }