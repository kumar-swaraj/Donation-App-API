from django.urls import path

from .views import categories, donation

app_name = 'donations'
urlpatterns = [
    path('categories/', categories),
    path('donations/<int:pk>/', donation),
]
