from rest_framework import serializers

from .models import Wishlist

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        # fields = "__all__"
        exclude = ['customer', 'modified', 'created']
        depth = 1
        read_only_fields = ['product', 'category',]


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['product'] = {
            "id": instance.product.id,
            "colors": instance.product.colors,
            "name": instance.product.name,
            "description": instance.product.description,
            "price": float(instance.product.price),
            "on_sale": instance.product.on_sale,
            "main_image": instance.product.get_image_url(),
            # "sale_percent": str(int(instance.product.sale_percent)) + "%",
            # "price_after_sale": instance.product.price_after_sale ,
            "category": {
                "name": instance.product.category.name
            }
        }

        if instance.product.on_sale:
            """
            if the product is on sale, we add the sale percent to the representation 
            the sale percent is a string and it is the percentage of the sale
            """
            representation['product']['sale_percent'] = str(int(instance.product.sale_percent)) + '%'
            representation['product']['price_after_sale'] = instance.product.price_after_sale

        return representation