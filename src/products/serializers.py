from rest_framework import serializers
from .models import Product, Category, ProductReport, ProductReview


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {
            "id": instance.category.id,
            "name": instance.category.name
        }
        return representation