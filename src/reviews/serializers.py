from rest_framework import serializers

from .models import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        # fields = "__all__"
        exclude = ["modified", "created", 'product', 'customer',]
        read_only_fields = ["id", "created", "modified"]
        extra_kwargs = {
            "rating": {"min_value": 1, "max_value": 5},
        }
    

