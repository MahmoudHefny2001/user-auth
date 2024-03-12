from django.contrib import admin

from .models import Product, Category, ProductAttachment

admin.site.register(Product)
admin.site.register(ProductAttachment)
admin.site.register(Category)