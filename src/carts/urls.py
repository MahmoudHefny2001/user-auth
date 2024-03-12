from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^my-cart", views.CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),    
]