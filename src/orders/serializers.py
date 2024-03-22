from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"



class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['order_items'] = OrderItemSerializer(instance.order_items.all(), many=True).data
        return representation
