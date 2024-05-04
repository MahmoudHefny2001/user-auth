from rest_framework import serializers

from .models import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        # fields = "__all__"
        exclude = ["modified", "created", 'customer',]
        read_only_fields = ["id", "created", "modified"]
        extra_kwargs = {
            "rating": {"min_value": 1, "max_value": 5},
        }
    

    # def to_representation(self, instance):
    #     # Overriding the to_representation method to return the product name instead of the product id
    #     response = super().to_representation(instance)
    #     response["product"] = instance.product.name
