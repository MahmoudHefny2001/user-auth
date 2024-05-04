from django.urls import path, include
from . import views


from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^for-merchants", views.ProductReviewViewSetForMerchants, basename="product-review-for-merchants")

router.register(r"", views.ProductReviewViewSet, basename="product-review")

urlpatterns = [
    path("", include(router.urls)),  
]
