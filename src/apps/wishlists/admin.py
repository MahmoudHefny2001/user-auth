from django.contrib import admin

from .models import Wishlist, WishlistItem


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created']
    search_fields = ['customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address', ]
    list_filter = ['customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address',]
    list_display_links = ['customer',]
    list_select_related = ['customer',]



class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['wishlist', 'product', 'created']
    search_fields = ['wishlist__customer__full_name', 'wishlist__customer__email', 'wishlist__customer__phone_number', 'wishlist__customer__address', 'product__name', 'product__price', 'product__image',]
    list_filter = ['wishlist__customer__full_name', 'wishlist__customer__email', 'wishlist__customer__phone_number', 'wishlist__customer__address', 'product__name', 'product__price', 'product__image',]
    list_display_links = ['wishlist', 'product',]
    list_select_related = ['wishlist', 'product',]


admin.site.register(Wishlist, WishlistAdmin)

admin.site.register(WishlistItem, WishlistItemAdmin)

