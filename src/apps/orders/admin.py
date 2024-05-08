from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'status', 'total_price', 'created',]
    search_fields = ['customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address', 'status', 'total_price',]
    list_filter = ['customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address', 'status', 'total_price',]
    list_display_links = ['customer', 'created']
    list_select_related = ['customer',]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)