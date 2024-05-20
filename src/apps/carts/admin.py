from django.contrib import admin

from .models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created']
    search_fields = ['customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address',]
    list_filter = ['customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address',]
    list_display_links = ['customer']
    list_select_related = ['customer', ]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'item_quantity', 'created']
    search_fields = ['cart__customer__full_name', 'cart__customer__email', 'cart__customer__phone_number', 'cart__customer__address',]
    list_filter = ['cart__customer__full_name', 'cart__customer__email', 'cart__customer__phone_number', 'cart__customer__address',]
    list_display_links = ['cart', 'product']
    list_select_related = ['cart', 'product', ]


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)

