from rest_framework import serializers

from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        # fields = "__all__"
        exclude = ['customer', 'created', 'modified',]
        depth = 1
        read_only_fields = ['product', 'category']


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['product'] = {
            "id": instance.product.id,
            "name": instance.product.name,
            "colors": instance.product.colors,
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