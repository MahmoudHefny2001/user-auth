from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ["order", 'modified']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = {
            "name": instance.product.name,
            "price": instance.product.price,
        }

        try: 
            request = self.context.get('request')
            representation['product']['image'] = request.build_absolute_uri(instance.product.image.url)
        except FileNotFoundError:
            representation['product']['image'] = None

        except ValueError:
            representation['product']['image'] = None
        
        except Exception:
            representation['product']['image'] = None
    
        return representation

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Order
        depth = 1
        exclude = ['modified', 'cart',]


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # check if there is products_ids in the request
        order_items = []
        try:
            order_items = OrderItem.objects.filter(order=instance)
        except OrderItem.DoesNotExist:
            order_items = None
        if order_items:
            representation['items'] = OrderItemSerializer(order_items, many=True).data
        

        return representation


class OrderSerializerForMerchants(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    

    class Meta:
        model = Order
        # fields = "__all__"
        exclude = ['modified']
        depth = 1


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        order_items = []
        try:
            merchant = self.context['request'].user.merchant
            try:
                order_items = OrderItem.objects.filter(order=instance, product__merchant=merchant)
            except Exception as e:
                print("Error: ", e) 

        except OrderItem.DoesNotExist:
            order_items = None
        if order_items:
            representation['items'] = OrderItemSerializer(order_items, many=True).data
        
        
        representation['total_price'] = sum([order_item.sub_total_price for order_item in order_items])
        
        

        representation['customer'] = {
            "id": instance.customer.id,
            "full_name": instance.customer.full_name,
            "phone_number": instance.customer.phone_number,
            "address": instance.customer.address,
        }

        return representation
    