from django_filters import rest_framework as filters
from django.db.models import Subquery

from .models import Activity, Collect
from beep.common.models import mm_Area

class ActivityFilter(filters.FilterSet):

    province_code = filters.CharFilter(field_name='province_code', method='province_code_filter', label='province_code')

    def province_code_filter(self, queryset, name, value):
        if name == 'province_code':
            if value == '-1': # 海外或全国地区筛选
                return queryset
            else:
                return queryset.filter(province_code=value)

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


