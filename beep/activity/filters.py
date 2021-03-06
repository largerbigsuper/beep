from django_filters import rest_framework as filters
from django.db.models import Subquery

from .models import Activity, Collect, RewardPlanApply, Registration, Schedule
from beep.common.models import mm_Area

class ActivityFilter(filters.FilterSet):

    city_name = filters.CharFilter(field_name='city_name', method='city_name_filter', label='city_name')

    def city_name_filter(self, queryset, name, value):
        if name == 'city_name':
            if value == '其他': # 海外或全国地区筛选
                qita = ['3301', '3101', '1101', '5101', '5001']
                return queryset.exclude(city_code__in=qita)
            else:
                return queryset.filter(city_name__icontains=value)

    class Meta:
        model = Activity
        fields = {
            'user_id': ['exact'],
            'activity_type': ['exact'],
            'province_code': ['exact'],
            'province_name': ['exact'],
            'city_code': ['exact'],
            'city_name': ['exact'],
            'district_code': ['exact'],
            'district_name': ['exact'],
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


class RewardPlanApplyFilter(filters.FilterSet):

    class Meta:
        model = RewardPlanApply
        fields = {
            'activity_id': ['exact'],
            'user': ['exact'],
            'rewardplan': ['exact'],
            'is_selected': ['exact'],
        }


class RegistrationFilter(filters.FilterSet):

    class Meta:
        model = Registration
        fields = {
            'activity__start_at': ['gt', 'lt'],
            'activity__end_at': ['gt', 'lt'],
        }


class ScheduleFilter(filters.FilterSet):

    class Meta:
        model = Schedule
        fields = {
            'user': ['exact'],
            'plan_datetime': ['gt', 'lt'],
        }