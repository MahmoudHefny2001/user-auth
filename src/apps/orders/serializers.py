from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = OrderItem
        # fields = "__all__"
        exclude = ["order", 'modified']



class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        # fields = "__all__"
        exclude = ['modified']
        depth = 1


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # check if there is products_ids in the request
        
        try:
            order_items = OrderItem.objects.get(order=instance)

            if order_items:
                representation['items'] = OrderItemSerializer(order_items, many=True).data
        except OrderItem.DoesNotExist:
            raise serializers.ValidationError("Order Items not found")

        representation['customer'] = {
            "id": instance.customer.id,
            "full_name": instance.customer.full_name,
            "phone_number": instance.customer.phone_number,
        }

        if instance.cart:
            representation['cart'] = {
                "id": instance.cart.id,
                "created": instance.cart.created,
                "item_quantity": instance.cart.item_quantity,
                "product": {
                    "name": instance.cart.product.name,
                    "price": instance.cart.product.price,
                    # "image": instance.cart.product.image
                }
            }

        return representation
