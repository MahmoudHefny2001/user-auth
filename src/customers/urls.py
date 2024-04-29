from django.urls import path, include
from . import views



from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"^profiles", views.CustomerProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", views.CustomerSignupView.as_view(), name="signup"),
    path("login/", views.CustomerLoginView.as_view(), name="login"),

    path("logout/", views.CustomerLogOutView.as_view(), name="logout"),

    path('token/refresh/', views.CustomerTokenRefreshView.as_view(), name='token_refresh'),

    path('password-update/', views.CustomerPasswordUpdateView.as_view(), name='password_update'),

    path('account-delete/', views.CustomerDeleteView.as_view(), name='account_delete'),


    path('password-reset-mail/', views.CustomerPasswordResetView.as_view(), name='password_reset_mail'),
    path('password-update-mail/', views.CustomerPasswordUpdateMailView.as_view(), name='password_reset'),

    # path('confirm-email/', views.CustomerEmailVerificationView.as_view(), name='email_verification'),

    # path('google-login/', views.GoogleSocialLoginView.as_view()),
    # path('google-signup/', views.GoogleSocialSignupView.as_view()),


]
