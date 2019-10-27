from django.urls import path

from . import consumers, echo_consumers, consumers_wehub, consumers_live

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
    path('ws/echo/', echo_consumers.EchoConsumer),
    path('ws/wehub/', consumers_wehub.WehubConsumer),
    path('ws/live/<str:room_name>/', consumers_live.LiveConsumer),

]