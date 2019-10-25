from django.urls import path

from . import consumers, echo_consumers, consumers_wehub

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
    path('ws/echo/', echo_consumers.EchoConsumer),
    path('ws/wehub/', consumers_wehub.EchoConsumer),
]