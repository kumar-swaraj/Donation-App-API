from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import logout, me, register

app_name = 'accounts'
urlpatterns = [
    path('profile/', me, name='profile'),
    path('auth/register/', register, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/logout/', logout, name='logout'),
]
