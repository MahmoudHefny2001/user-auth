from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^my-cart", views.CartViewSet, basename="customer-cart")

router.register(r"^clear-cart", views.ClearCartViewSet, basename="clear-cart")

urlpatterns = [
    
    path("", include(router.urls)),
    
]