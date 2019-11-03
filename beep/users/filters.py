from django_filters import rest_framework as filters
from django_filters.rest_framework import NumberFilter

from .models import User

class UserFilter(filters.FilterSet):

    user_id = NumberFilter(field_name='user_id', method='user_id_filter', label='user_id')

    def user_id_filter(self, queryset, name, value):
        return queryset

    class Meta:
        model = User
        fields = {
            'user_id': ['exact'],
            'name': ['exact', 'icontains'],
            'account': ['icontains'],
        }