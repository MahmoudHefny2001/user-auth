from django.contrib import admin

from .models import Product, Category, ProductAttachment, ProductReport, ProductReview

admin.site.register(Product)
admin.site.register(ProductAttachment)
admin.site.register(Category)