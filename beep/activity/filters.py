from django_filters import rest_framework as filters
from django.db.models import Subquery

from .models import Activity, Collect
from beep.common.models import mm_Area

class ActivityFilter(filters.FilterSet):

    city_code = filters.CharFilter(field_name='city_code', method='city_code_filter', label='city_code')

    def city_code_filter(self, queryset, name, value):
        if name == 'city_code':
            if value == '-1': # 海外或全国地区筛选
                qita = ['3301', '3101', '1101', '5101', '5001']
                return queryset.exclude(city_code__in=qita)
            else:
                return queryset.filter(city_code=value)

    class Meta:
        model = Activity
        fields = {
            'user_id': ['exact'],
            'activity_type': ['exact'],
            'province_code': ['exact'],
            'city_code': ['exact'],
            'district_code': ['exact'],
            'title': ['icontains'],
            'ticket_price': ['gte', 'lte'],
            'start_at': ['iexact', 'gte', 'lte'],
            'start_at': ['iexact', 'gte', 'lte'],
            'create_at': ['iexact', 'gte', 'lte'],
        }

class CollectFilter(filters.FilterSet):

    class Meta:
        model = Collect

        fields = {
            'activity_id': ['exact'],
        }


