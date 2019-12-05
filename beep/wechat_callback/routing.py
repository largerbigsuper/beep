from django.urls import path

from . import consumers_wehub, consumers_live, consumers_wehub_task

websocket_urlpatterns = [
    path('ws/wehub/', consumers_wehub.WehubConsumer),
    path('ws/wehub_task/', consumers_wehub_task.WehubTaskConsumer),
    path('ws/live/<str:room_name>/', consumers_live.LiveConsumer),
]