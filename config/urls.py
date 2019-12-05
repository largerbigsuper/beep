from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Beep API",
      default_version='v1',
      description="Beep Rest API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="zaihuazhao@163.com"),
      license=openapi.License(name="Not Open Source"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


from .router_user import router_user
from .router_admin import router_admin
from beep.wechat_callback import views as wehub_views
from beep.common import views as common_views
from .views import index

urlpatterns = [
    # path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('', index),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-user/', include(router_user.urls)),
    # path('api-admin/', include(router_admin.urls)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('socket/', wehub_views.socket_test),
    path('wehub_api/', wehub_views.wehub_api),
    path('upload_file/', wehub_views.upload_file),
    path('coindata/', common_views.data_ticker),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

admin.site.site_header = 'beep后台管理'