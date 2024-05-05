from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response

from .models import Order, OrderItem

from .serializers import OrderSerializer, OrderItemSerializer, OrderSerializerForMerchants

from apps.carts.models import Cart

from rest_framework_simplejwt.authentication import JWTAuthentication


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
                return self.queryset.filter(customer=customer)
            except Exception as e:
                print(e)
    
    def create(self, request, *args, **kwargs):

        # Check if the user has a customer profile
        if not request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve products from the request data
        products_ids = request.data.get("products_ids", [])
        

        if products_ids:
            # If products are provided directly in the request, return an error
            return Response({"error": "You cannot provide products directly. Use your cart to create an order."}, status=status.HTTP_400_BAD_REQUEST)


        else:
            # Check if the user has items in the cart
            cart = Cart.objects.filter(customer=request.user.customer).first()

            
            
            if not cart:
                return Response({"error": "Your cart is empty. Add products to make an order or use your existing cart."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if cart items are available and update stock
            for cart in Cart.objects.filter(customer=request.user.customer):
                if cart.item_quantity < 1 or not cart.product.available or cart.item_quantity > cart.product.quantity:
                    return Response({"error": f"{cart.product.name} is not available in the required quantity"}, status=status.HTTP_400_BAD_REQUEST)
                cart.product.quantity -= cart.item_quantity
                cart.product.save()
                if cart.product.quantity < 1:
                    cart.product.available = False
                    cart.product.save()


            # Check if the user has a shipping address
            customer = request.user.customer
            
            if not (customer.address or request.data.get("shipping_address")):
                return Response({"error": "You need to add your address to your profile or specify a shipping address before making an order"}, status=status.HTTP_400_BAD_REQUEST)

            # Create order based on cart items
            order = Order.objects.create(
                customer=request.user.customer,
                total_price=cart.total(),
                shipping_address=request.data.get("shipping_address", None),
                payment_method=request.data.get("payment_method",) if request.data.get("payment_method",) else Order.PaymentMethod.CASH_ON_DELIVERY,
                cart=cart
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

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    

    

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()

    #     if instance.customer != request.user.customer:
    #         return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     order = serializer.save()


    #     return Response(OrderSerializer(order).data)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        

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
    
    