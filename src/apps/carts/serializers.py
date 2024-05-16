from rest_framework import serializers

from .models import Cart, CartItem

import os

HOST_URL = os.environ.get('HOST_URL')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ['created', 'modified', 'cart']
        read_only_fields = ['product', 'category']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = {
            "id": instance.product.id,
            "name": instance.product.name,
            "price": instance.product.price,
            "merchant": {
                "business_name": instance.product.merchant.full_name,
            }
            
        }

        if instance.product.category:
            representation['product']['category'] = {
                "id": instance.product.category.id,
                "name": instance.product.category.name,
            }
        
        if instance.product.get_colors():
            representation['product']['color'] = {
                "id": instance.product.color.id,
                "name": instance.product.color.name,
                "code": instance.product.color.code,
            }
        
        if instance.product.image:
            representation['product']['image'] = instance.product.image.url
            # representation['product']['image'] = str(HOST_URL) + instance.product.image.url
        
        return representation


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        # fields = "__all__"
        exclude = ['customer', 'created', 'modified',]
        depth = 1


    