from rest_framework import serializers

from .models import Order, OrderItem

import os


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ["order", 'modified', 'created']
    
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

        try:
            # representation['product']['image'] = str(os.environ.get('HOST_URL') + instance.product.image.url)
            representation['product']['image'] = instance.product.image.url 
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
            try:
                # Retrieve merchant from the context
                merchant = self.context.get('request').user.merchant
                order_items = OrderItem.objects.filter(order=instance, product__merchant=merchant)
            except Exception as e:
                print("Error: ", e) 

        except OrderItem.DoesNotExist:
            order_items = None
        if order_items:
            representation['items'] = OrderItemSerializer(order_items, many=True).data
            # delete the merchant from the product 
            for item in representation['items']:
                del item['product']['merchant']

        
        representation['total_price'] = sum([order_item.sub_total_price for order_item in order_items])
        
        

        representation['customer'] = {
            "full_name": instance.customer.full_name,
            "phone_number": instance.customer.phone_number,
            "address": instance.customer.address,
        }


        del representation['cart']



        return representation
    