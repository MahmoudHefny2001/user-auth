from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^products", views.ProductViewSet, basename="products")


urlpatterns = [
    path("", include(router.urls)),
    path('home/', views.HomeViewSet.as_view(), name='home'),
]