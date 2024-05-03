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
            "name": instance.product.name,
            "description": instance.product.description,
            "price": float(instance.product.price),
            "on_sale": instance.product.on_sale,
            "main_image": instance.product.image,

        }

        if instance.product.on_sale:
            """
            if the product is on sale, we add the sale percent to the representation 
            the sale percent is a string and it is the percentage of the sale
            """
            representation['product']['sale_percent'] = str(int(instance.product.sale_percent)) + '%'
            representation['product']['price_after_sale'] = instance.product.price_after_sale

        if instance.product.category:
            """
            if the product has a category, we add the category to the representation
            """
            representation['product']['category'] = {
                "id": instance.product.category.id,
                "name": instance.product.category.name,
            }
        
        # product colors from the productColor Model that have a foreign key to the product
        from apps.products.models import ProductColor
        
        try:
            colors = ProductColor.objects.filter(product=instance.product)

        except ProductColor.DoesNotExist:
            colors = None
        if colors:
            """
            if the product has colors, we add the colors to the representation
            """
            representation['product']['colors'] = []
            for color in colors:
                representation['colors'].append(
                    {
                        "color": color,
                    }
                )

        else:
            representation['product']['colors'] = []

        return representation