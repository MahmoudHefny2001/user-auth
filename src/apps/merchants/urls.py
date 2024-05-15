from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^profiles", views.MerchantProfileViewSet, basename="profiles")


router.register(r"^all", views.MerchantViewSet, basename="merchants")

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", views.MerchantSignupView.as_view(), name="signup"),
    path("login/", views.MerchantLoginView.as_view(), name="login"),
 
    path("logout/", views.MerchantLogOutView.as_view(), name="logout"),
 
    path('token/refresh/', views.MerchantTokenRefreshView.as_view(), name='token_refresh'),

    path('account-delete/', views.MerchantDeleteView.as_view(), name='account_delete'),

    path('password-update/', views.MerchantPasswordUpdateView.as_view(), name='password_update'),

    path('password-reset-mail/', views.MerchantPasswordResetMailView.as_view(), name='password_reset'),
    path('forget-password-mail/', views.MerchantPasswordUpdateMailView.as_view(), name='password_reset_mail'),

    # path('confirm-email/', views.MerchantEmailVerificationView.as_view(), name='email_verification'),

]

