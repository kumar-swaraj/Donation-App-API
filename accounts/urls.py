from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import me, register

app_name = 'accounts'
urlpatterns = [
    path('me/', me),
    path('auth/register/', register),
    path('auth/login/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
]
