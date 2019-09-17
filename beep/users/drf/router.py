from rest_framework import routers

from .viewsets import UserViewSet

router_users = routers.DefaultRouter()

router_users.register('', UserViewSet, base_name='users')
