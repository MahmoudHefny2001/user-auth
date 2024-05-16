from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response

from .serializers import OrderSerializer, OrderSerializerForMerchants


from apps.carts.models import Cart
from apps.products.models import Product

from .models import Order, OrderItem

from rest_framework_simplejwt.authentication import JWTAuthentication

from .mail import send_customer_order_email, send_merchant_order_email

from .tasks import update_product_quantity_and_availability, clear_cart

from django.db import transaction

import threading



class OrderViewSetForCustomers(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'order_id', 'order_name', 'extra_notes', 'shipping_address',]

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]


    def get_queryset(self):
        customer = None
        try:
            customer = self.request.user.customer
        except AttributeError:
            return self.queryset.none()
            
        if customer:

            try:
                # if no order items are found, the queryset will be empty so return an empty queryset
                if not OrderItem.objects.filter(order__customer=customer):
                    return self.queryset.none()
                # return OrderItem.objects.filter(order__customer=customer).values_list('order', flat=True)
                return Order.objects.filter(order_items__order__customer=customer).distinct()
            except Exception as e:
                print(e)
    

    def create(self, request, *args, **kwargs):
        
        try:
            customer = request.user.customer

            if not customer:
                return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

            cart = Cart.objects.prefetch_related('cart_items').get(customer=customer)

            if not cart:
                return Response({"error": "Your cart is empty. Add products to make an order or use your existing cart."}, status=status.HTTP_400_BAD_REQUEST)

            shipping_address = request.data.get("shipping_address")

            if not shipping_address:
                if not customer.address:
                    return Response({"error": "You need to add your address to your profile or specify a shipping address before making an order"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    shipping_address = customer.address

            with transaction.atomic():
                # Create the order
                order = Order.objects.create(
                    customer=customer,
                    shipping_address=shipping_address,
                    payment_method=request.data.get("payment_method", Order.PaymentMethod.CASH_ON_DELIVERY)
                )

                # Prepare a list of OrderItem objects to be created in bulk
                order_items = []
                total_price = 0  # Initialize total_price

                for cart_item in cart.cart_items.all():
                    sub_total_price = cart_item.get_sub_total()  # Calculate sub_total_price
                    total_price += sub_total_price  # Add to total_price
                    order_items.append(OrderItem(
                        order=order,  # Set the order attribute
                        product=cart_item.product,
                        quantity=cart_item.item_quantity,
                        sub_total_price=sub_total_price
                    ))

                # Bulk create OrderItems
                OrderItem.objects.bulk_create(order_items)

                # Set the total_price for the order
                order.total_price = total_price
                order.save()

                # Other actions (sending emails, updating product quantity, clearing cart)
                # Send emails to the merchant and the customer non-blocking using Celery with a new thread
                thread1 = threading.Thread(target=send_merchant_order_email, args=(order,))
                thread1.start()

                thread2 = threading.Thread(target=send_customer_order_email, args=(order,))
                thread2.start()
                
                thread3 = threading.Thread(target=update_product_quantity_and_availability, args=(order,))
                thread3.start()
                
                thread4 = threading.Thread(target=clear_cart, args=(cart,))
                thread4.start()

                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({"error": "Your cart does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        shipping_address = request.data.get("shipping_address", None)
        payment_method = request.data.get("payment_method", None)
        extra_notes = request.data.get("extra_notes", None)

        if shipping_address:
            instance.shipping_address = shipping_address
        if payment_method:
            instance.payment_method = payment_method
        if extra_notes:
            instance.extra_notes = extra_notes

        instance.save()

        return Response(OrderSerializer(instance).data, status=status.HTTP_200_OK)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        

        with transaction.atomic():
            order_items = OrderItem.objects.filter(order=instance)

            for order_item in order_items:
                
                product = order_item.product
                
                product.quantity += order_item.quantity
                
                if product.quantity > 0:
                    product.available = True
                
                product.save()

                order_item.delete()
            

            self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)




class OrderViewSetForMerchants(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializerForMerchants
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'order_id', 'order_name', 'extra_notes', 'shipping_address',]

    http_method_names = ['get', 'retrieve', 'patch',]

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    def get_queryset(self):
        if not self.request.user.merchant:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        self.queryset = Order.objects.filter(order_items__product__merchant=self.request.user.merchant).distinct()
        return self.queryset
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()


        order_status = request.data.get("status", None)
        if status:
            instance.status = order_status
            instance.save()
            return Response(OrderSerializerForMerchants(instance).data)
        return Response({"error": "You need to provide a status to update the order"}, status=status.HTTP_400_BAD_REQUEST)



class SingleProductOrderView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]
    


    def create(self, request, *args, **kwargs):

        customer = request.user.customer

        product_id = request.data.get("product_id")
        
        if not product_id:
            return Response({"error": "You need to provide the product to make the order"}, status=status.HTTP_400_BAD_REQUEST)
        

        product = Product.objects.get(id=product_id)
        
        quantity = request.data.get("quantity", 1)

        if not product:
            return Response({"error": "The product does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if not product.available:
            return Response({"error": "The product is not available"}, status=status.HTTP_400_BAD_REQUEST)
        
        if product.quantity < quantity:
            return Response({"error": "The quantity of the product is not enough"}, status=status.HTTP_400_BAD_REQUEST)
        

        if not customer.address:
            if not request.data.get("shipping_address"):
                return Response({"error": "You need to add your address to your profile or specify a shipping address before making an order"}, status=status.HTTP_400_BAD_REQUEST)
            

        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                total_price=product.price * quantity,
                shipping_address=request.data.get("shipping_address", customer.address),
                payment_method=request.data.get("payment_method", Order.PaymentMethod.CASH_ON_DELIVERY),
            )

            order.save()

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                sub_total_price=product.price * quantity
            )

            order_item.save()

            product.quantity -= quantity
            
            if product.quantity <= 0:
                product.available = False

            product.save()

            try:
                # Send emails to the merchant and the customer non-blocking using Celery
                thread1 = threading.Thread(target=send_merchant_order_email, args=(order,))
                thread1.start()
                thread2 = threading.Thread(target=send_customer_order_email, args=(order,))
                thread2.start()
            except Exception as e:
                pass

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        shipping_address = request.data.get("shipping_address", None)
        payment_method = request.data.get("payment_method", None)
        extra_notes = request.data.get("extra_notes", None)

        if shipping_address:
            instance.shipping_address = shipping_address
        if payment_method:
            instance.payment_method = payment_method
        if extra_notes:
            instance.extra_notes = extra_notes

        instance.save()

        return Response(OrderSerializer(instance).data, status=status.HTTP_200_OK)




class OrderItemCancellationView(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    def post(self, request, *args, **kwargs):
        order_item_id = kwargs.get("pk")

        try:
            order_item = OrderItem.objects.get(id=order_item_id, order__customer=request.user.customer)
        except OrderItem.DoesNotExist:
            return Response({"error": "The order item does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = order_item.order
        except Order.DoesNotExist:
            return Response({"error": "The order does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not order_item:
            return Response({"error": "The order item does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        

        if order_item.order.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)


        product = order_item.product

        product.quantity += order_item.quantity

        if product.quantity > 0:
            product.available = True

        product.save()

        order_item.delete()

        # Update the total price of the order
        try:
            order.total_price = sum([order_item.sub_total_price for order_item in OrderItem.objects.filter(order=order)])
            order.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "The order item has been canceled successfully"}, status=status.HTTP_200_OK)



