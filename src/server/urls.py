from django.contrib import admin

from django.urls import path, include, re_path  #

from django.conf.urls.static import static

from rest_framework import permissions

from django.conf import settings

from django.views.static import serve

from drf_yasg.views import get_schema_view

from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Digital Hub API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("customers/", include("apps.customers.urls")), #

    path("api/", include("apps.products.urls")), #

    path("contact-us/", include("apps.contacts.urls")), #

    path("wishlists/", include("apps.wishlists.urls")), #

    path("carts/", include("apps.carts.urls")), #

    path("reviews/", include("apps.reviews.urls")), #

    path("merchants/", include("apps.merchants.urls")), #

    path("orders/", include("apps.orders.urls")), #

    path("payments/", include("apps.payments.urls")), #

    path('api-documentation/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'), #

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    