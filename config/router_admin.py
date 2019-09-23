from rest_framework import routers

from beep.news import viewsets as news_viewset

router_admin = routers.DefaultRouter()

router_admin.register('news', news_viewset.AdminNewsViewSet, base_name='admin-news')
