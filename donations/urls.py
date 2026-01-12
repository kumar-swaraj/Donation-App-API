from django.urls import path

from .views import categories, donation, health_check

app_name = 'donations'
urlpatterns = [
    path('health/', health_check),
    path('categories/', categories),
    path('donations/<int:pk>/', donation),
]
