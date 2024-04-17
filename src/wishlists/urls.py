from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^my-wishlist", views.WishListViewSet, basename="wishlist")

urlpatterns = [
    path("", include(router.urls)),
    
]