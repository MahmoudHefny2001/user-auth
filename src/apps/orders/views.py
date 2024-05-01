from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response

from .models import Order, OrderItem

from .serializers import OrderSerializer, OrderItemSerializer

from apps.carts.models import Cart


class OrderViewSetForCustomers(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'order_id', 'order_name', 'extra_notes', 'shipping_address',]

    def get_queryset(self):
        customer = None
        try:
            customer = self.request.user.customer
        except AttributeError:
            return self.queryset.none()
            
        if customer:
            return self.queryset.filter(customer=customer)
        
    
    def create(self, request, *args, **kwargs):
        if not request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(customer=request.user.customer)


        headers = self.get_success_headers(serializer.data)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED, headers=headers)
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()


        return Response(OrderSerializer(order).data)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)




class OrderItemViewSetForCustomers(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['order', 'product', 'quantity',]

    def get_queryset(self):
        return self.queryset.filter(order__customer=self.request.user.customer)
    
    def create(self, request, *args, **kwargs):
        if not request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        

        # Check if products in the cart or order in general are available or not and also the quantity required is less than or equal to the quantity available
        cart = Cart.objects.filter(customer=request.user.customer).first()
        if not cart:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        product = cart.product

        if product.quantity < cart.quantity or product.quantity < 1 or not product.available:
            return Response({"error": "Product is not available in the required quantity"}, status=status.HTTP_400_BAD_REQUEST)


        order_item = OrderItem.objects.filter(product=product).first()

        if product.quantity < order_item.quantity or product.quantity < 1 or not product.available:
            return Response({"error": "Product is not available in the required quantity"}, status=status.HTTP_400_BAD_REQUEST)
        

        if order_item:
            product.quantity -= order_item.quantity
            product.save()

            if product.quantity < 1:
                product.available = False
                product.save()
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()

        headers = self.get_success_headers(serializer.data)

        return Response(OrderItemSerializer(order_item).data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.order.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)


        if instance.product.quantity < instance.quantity or instance.product.quantity < 1 or not instance.product.available:
            return Response({"error": "Product is not available in the required quantity"}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()



        return Response(OrderItemSerializer(order_item).data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.order.customer != request.user.customer:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)


        # after destroying the order item, the quantity of the product should be restored
        product = instance.product
        product.quantity += instance.quantity
        product.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



class OrderViewSetForMerchants(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'order_id', 'order_name', 'extra_notes', 'shipping_address',]

    http_method_names = ['get', 'retrieve',]

    def get_queryset(self):
        return self.queryset.filter(cart__merchant=self.request.user.merchant)
    
    