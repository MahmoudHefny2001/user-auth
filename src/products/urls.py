from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^products", views.ProductViewSet, basename="products")

router.register(r"^products-favourite", views.FavouriteProducts, basename="favourite_products")



urlpatterns = [
    path("", include(router.urls)),
    path('home/', views.HomeViewSet.as_view(), name='home'),
]