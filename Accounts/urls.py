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
    path('user/login/', views.UserLoginView.as_view(), name='user_login'),
    path('change/password/', views.ChangePasswordUser.as_view(), name='user_change_password'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNTIyODM3OSwiaWF0IjoxNzMyNjM2Mzc5LCJqdGkiOiJlMWUxY2FkZjNhMmI0MTJjYjhhOWRjYWNmMzNjZDM2ZCIsInVzZXJfaWQiOjQyfQ.RrMTeyHOhy9CI5y3e0SyFLGVj9XqTruSzkvS4r88K_c",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyNzIyNzc5LCJpYXQiOjE3MzI2MzYzNzksImp0aSI6IjhhZTFhMGI1M2YxMzQzZjE4NGY2NTUwMjNmMjY1ZWU3IiwidXNlcl9pZCI6NDJ9.azq77fLupCqjgJvh_OJNmWzlM_8Aa4ROTeMHvE3tqoc"
# }
