from django.urls import include, path
from rest_framework import routers
from appaccount import views
from rest_framework.urlpatterns import format_suffix_patterns

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('users/', views.UserViewSet.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns = format_suffix_patterns(urlpatterns)
