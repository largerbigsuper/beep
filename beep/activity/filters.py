from django_filters import rest_framework as filters

from .models import Activity, Collect

class ActivityFilter(filters.FilterSet):

    class Meta:
        model = Activity
        fields = {
            'user_id': ['exact'],
            'activity_type': ['exact'],
            'area__parent_id': ['exact'],
            'area_id': ['exact'],
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


