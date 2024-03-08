from rest_framework import serializers
from .models import Product, Category, ProductReport, ProductReview, ProductAttachment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = "__all__"
        exclude = ['created', 'modified',]



class GetProductsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ['created', 'modified', 'quantity',]
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {
            "id": instance.category.id,
            "name": instance.category.name
        }
        representation['sale_percent'] = str(int(instance.sale_percent)) + '%'
        return representation
    


class RetrieveProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ['created', 'modified', 'quantity']
        depth = 2

    product_attachments = []
# 
    for attachment in ProductAttachment.objects.select_related('product').all():
        product_attachments.append(attachment.get_attachment_url())

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {
            "id": instance.category.id,
            "name": instance.category.name
        }
        representation['sale_percent'] = str(int(instance.sale_percent)) + '%'
        representation['images'] = list(self.product_attachments)
        return representation
    

from customers.models import CustomerFavouriteProduct


## HANDLE DELETE FAVOURITE PRODUCTS

class GetFavouriteProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFavouriteProduct
        # fields = "__all__"
        exclude = ['customer', ]
        depth = 1
        read_only_fields = ['product', 'category']


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['product'] = {
            "id": instance.product.id,
            "name": instance.product.name,
            "description": instance.product.description,
            "price": float(instance.product.price),
            "on_sale": instance.product.on_sale,
            "main_image": instance.product.get_image_url(),
            "sale_percent": str(int(instance.product.sale_percent)) + "%",
            "price_after_sale": instance.product.price_after_sale ,
            "category": {
                "name": instance.product.category.name
            }
        }

        return representation