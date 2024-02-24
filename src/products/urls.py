from django.urls import path, include
from . import views


urlpatterns = [
    path('home/', views.HomeViewSet.as_view(), name='home'),
]