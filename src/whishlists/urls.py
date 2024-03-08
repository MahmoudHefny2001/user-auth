from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^my-whishlist", views.WhishList, basename="favourite_products")

urlpatterns = [
    path("", include(router.urls)),
    
]