from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response

from .models import Order, OrderItem

from .serializers import OrderSerializer, OrderItemSerializer, OrderSerializerForMerchants

from apps.carts.models import Cart

from rest_framework_simplejwt.authentication import JWTAuthentication

from .mail import send_customer_order_email, send_merchant_order_email

class OrderViewSetForCustomers(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'order_id', 'order_name', 'extra_notes', 'shipping_address',]

    def get_queryset(self):
        customer = None
        try:
            customer = self.request.user.customer
        except AttributeError:
            return self.queryset.none()
            
        if customer:            

            try:
                return self.queryset.filter(customer=customer).exclude(status=Order.OrderStatus.CANCELED)
            except Exception as e:
                print(e)
    

    def create(self, request, *args, **kwargs):

        # Check if the user has a customer profile
        if not request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)


        customer = request.user.customer

        shipping_address = None

        cart = Cart.objects.filter(customer=request.user.customer).first()
        
        if not cart:
            return Response({"error": "Your cart is empty. Add products to make an order or use your existing cart."}, status=status.HTTP_400_BAD_REQUEST)


        if not customer.address:
            shipping_address = request.data.get("shipping_address")

            if not shipping_address: 
                return Response({"error": "You need to add your address to your profile or specify a shipping address before making an order"}, status=status.HTTP_400_BAD_REQUEST)


        # Check if cart items are available and update stock
        for cart in Cart.objects.filter(customer=request.user.customer):
            
            product = cart.product
            
            if not product.available or cart.item_quantity > product.quantity:
                return Response({"error": f"{cart.product.name} is not available in the required quantity"}, status=status.HTTP_400_BAD_REQUEST)
            
            product.quantity -= cart.item_quantity
            
            if product.quantity < 1:
                product.available = False
                product.save()

            product.save()
            
            cart.save()

        

        
        order = Order.objects.create(
            customer=request.user.customer,
            total_price=sum([cart.product.price for cart in Cart.objects.filter(customer=request.user.customer)]),
            shipping_address=shipping_address,
            cart=cart,
            # if not provided, the default set it to be the default payment method, if sent, it will be the provided payment method
            payment_method=request.data.get("payment_method", Order.PaymentMethod.CASH_ON_DELIVERY),
        )

        customer_carts = Cart.objects.filter(customer=customer)

        # Retrieve products associated with the carts
        customer_carts_products = [cart.product for cart in customer_carts]
        
        for product in customer_carts_products:
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart.item_quantity,
                sub_total_price=cart.product.price
            )
            order_item.save()
        
    
        order.total_price = sum([order_item.sub_total_price for order_item in OrderItem.objects.filter(order=order)])

        order.save()
    
        # Send emails to the merchant and the customer non-blocking using Celery
        send_merchant_order_email(order,)
        send_customer_order_email(order,)
        
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
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
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

    http_method_names = ['get', 'retrieve',]

    def get_queryset(self):
        if not self.request.user.merchant:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        return self.queryset.filter(cart__product__merchant=self.request.user.merchant)
    
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.cart.product.merchant != request.user.merchant:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        status = request.data.get("status", None)
        if status:
            instance.status = status
            instance.save()
            return Response(OrderSerializerForMerchants(instance).data)
        return Response({"error": "You need to provide a status to update the order"}, status=status.HTTP_400_BAD_REQUEST)
    