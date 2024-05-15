from django.contrib import admin

from .models import Product, Category, ProductAttachment


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'quantity', 'category', 'available', 'on_sale', 'sale_percent', 'price_after_sale', 'average_rating', 'merchant']
    search_fields = ['name', 'category__name', 'merchant__name']
    list_filter = ['category', 'available', 'on_sale', 'merchant']
    list_editable = ['price', 'quantity', 'available', 'on_sale', 'sale_percent', 'price_after_sale', 'merchant']
    list_display_links = ['name']
    list_select_related = ['category', 'merchant']
   
    

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttachment)
admin.site.register(Category)