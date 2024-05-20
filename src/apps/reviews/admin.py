from django.contrib import admin

from .models import ProductReview


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'rating', 'created']
    search_fields = ['product__name', 'customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address', 'rating', 'review',]
    list_filter = ['product__name', 'customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address', 'rating', 'review',]
    list_display_links = ['product', 'customer']
    list_select_related = ['product', 'customer', ]

admin.site.register(ProductReview, ProductReviewAdmin)