from rest_framework import routers

from beep.users import viewsets as user_viewsets
from beep.common import viewsets as common_viewsets
from beep.activity import viewsets as activity_viewsets
from beep.blog import viewsets as blog_viewsets

router_user = routers.DefaultRouter()

router_user.register('u', user_viewsets.UserViewSet, base_name='user-users')
router_user.register('schedule', user_viewsets.ScheduleViewSet, base_name='user-schedule')
router_user.register('checkin', user_viewsets.CheckInViewSet, base_name='user-checkin')
router_user.register('point', user_viewsets.PointViewSet, base_name='user-point')
router_user.register('area', common_viewsets.AreaViewSet, base_name='user-area')
router_user.register('activity', activity_viewsets.ActivityViewSet, base_name='user-activity')
router_user.register('topic', blog_viewsets.TopicViewSet, base_name='user-topic')
router_user.register('blog', blog_viewsets.BlogViewSet, base_name='user-blog')
router_user.register('atmsg', blog_viewsets.AtMessageViewSet, base_name='user-atmsg')
router_user.register('like', blog_viewsets.LikeViewSet, base_name='user-like')
router_user.register('comment', blog_viewsets.CommentViewSet, base_name='user-comment')
