from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    TokenVerifyView
)
app_name = 'accounts'


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('create/user/', views.UserCreate.as_view(), name='create_user'),
    path('profile/', views.UserProfileDetail.as_view(), name='user_profile'),
    path('user/logout/', views.UserLogoutViews.as_view(), name='user_logout'),

]
