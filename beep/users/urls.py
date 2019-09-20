from django.urls import path, include

from beep.users.drf.router import router_users

urlpatterns = [
        path('', include(router_users.urls)),
]
