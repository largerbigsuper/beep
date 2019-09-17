from django.urls import path, include

from get_the_channel.users.drf.router import router_users

urlpatterns = [
        path('', include(router_users.urls)),
]
