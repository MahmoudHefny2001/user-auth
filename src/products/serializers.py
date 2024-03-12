from rest_framework import serializers
from .models import Product, Category, ProductAttachment


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
        representation['average_rating'] = instance.average_rating
        representation['sale_percent'] = str(int(instance.sale_percent)) + '%'
        return representation
    


class RetrieveProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ['created', 'modified', 'quantity']
        depth = 2

    def to_representation(self, instance):

        product_attachments = []
# 
        for attachment in ProductAttachment.objects.select_related('product').all():
            product_attachments.append(attachment.get_attachment_url())

        representation = super().to_representation(instance)
        representation['category'] = {
            "id": instance.category.id,
            "name": instance.category.name
        }
        representation['sale_percent'] = str(int(instance.sale_percent)) + '%'
        representation['images'] = list(product_attachments)

        representation['average_rating'] = instance.average_rating
        representation['reviews'] = instance.get_reviews()

        return representation
    


