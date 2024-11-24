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
    path('change/password/', views.ChangePasswordUser.as_view(), name='user_change_password'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-req'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-rest-confirm'),
]


# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNTA0NzU3MywiaWF0IjoxNzMyNDU1NTczLCJqdGkiOiI1ZTYyMzgxNWFlYzA0YzMxODE2OTk0ZDUyOGU5MGI3ZiIsInVzZXJfaWQiOjJ9.G9rl3g_PmxLBRTecc8HVl4-cFzc25aKJ-oQTyFP2BJs",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyNTQxOTczLCJpYXQiOjE3MzI0NTU1NzMsImp0aSI6ImI5ZGQ1YTdjZWYxYzRiZTRhYWVhMTk4NGQyNzg1MTJhIiwidXNlcl9pZCI6Mn0.9Y7aiP5wOGFmLLkRXgXdF0QIgm9n_eptQp-A5NYJX6M"
# }