from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^my-wishlist", views.WishList, basename="favourite_products")

urlpatterns = [
    path("", include(router.urls)),
    
]