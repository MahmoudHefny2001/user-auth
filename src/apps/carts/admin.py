from django.contrib import admin

from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product',]
    search_fields = ['customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address', 'product__name', 'product__category__name',]
    list_filter = ['customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address', 'product__name', 'product__category__name',]
    list_display_links = ['customer', 'product']
    list_select_related = ['customer', 'product']


admin.site.register(Cart, CartAdmin)
