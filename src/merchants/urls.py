from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^profiles", views.MerchantProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", views.MerchantSignupView.as_view(), name="signup"),
    path("login/", views.MerchantLoginView.as_view(), name="login"),
 
    # path("logout/", views.MerchantLogOutView.as_view(), name="logout"),
 
    # path('token/refresh/', views.MerchantTokenRefreshView.as_view(), name='token_refresh'),

    # path('account-delete/', views.MerchantDeleteView.as_view(), name='account_delete'),

]

