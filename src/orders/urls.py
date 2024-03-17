from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register(r"customer-orders", views.OrderViewSetForCustomers, basename="customer-orders")
# router.register(r"merchant-orders", views.OrderViewSetForMerchants, basename="merchant-orders")

urlpatterns = [
    path("", include(router.urls)),
    
]