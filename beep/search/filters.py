from datetime import date, timedelta

import django_filters
from django_filters import rest_framework as filters

from .models import SearchKeyWord


class SearchKeyWordFilter(filters.FilterSet):

    passed_day = django_filters.NumberFilter(field_name='create_date', method='filter_passed_day')

    def filter_passed_day(self, queryset, name, value):
        
        return queryset.filter(create_date__gte=date.today() - timedelta(days=int(value)))

    class Meta:
        model = SearchKeyWord
        fields = ['passed_day']

