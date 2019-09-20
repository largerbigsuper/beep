from rest_framework import routers

from beep.users import viewsets as user_viewsets
from beep.common import viewsets as common_viewsets
from beep.activity import viewsets as activity_viewsets

router_user = routers.DefaultRouter()

router_user.register('u', user_viewsets.UserViewSet, base_name='user-users')
router_user.register('schedule', user_viewsets.ScheduleViewSet, base_name='user-schedule')
router_user.register('checkin', user_viewsets.CheckInViewSet, base_name='user-checkin')
router_user.register('point', user_viewsets.PointViewSet, base_name='user-point')
router_user.register('area', common_viewsets.AreaViewSet, base_name='user-area')
router_user.register('activity', activity_viewsets.ActivityViewSet, base_name='user-activity')

# router_user.register('blog', BlogViewSet, base_name='user-blog')