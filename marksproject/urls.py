
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from appaccount.views import CheckExpireToken
from appaccount.tokenserializiers import(MyTokenObtainPairView)
# from rest_framework.authtoken import views


urlpatterns = [
    # path('api-token-auth/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('api/checktoken/', CheckExpireToken.as_view(),
         name='hello'),  # check token validate
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Api USER
    path('api/', include('appaccount.urls')),
    path('api/', include('appmarks.urls')),

]
