from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response

from .models import Order, OrderItem

from .serializers import OrderSerializer, OrderItemSerializer




class OrderViewSetForCustomers(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'order_id', 'order_name', 'extra_notes', 'shipping_address',]

    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user.customer)
    
    def create(self, request, *args, **kwargs):
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




class OrderViewSetForMerchants(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'order_id', 'order_name', 'extra_notes', 'shipping_address',]

    def get_queryset(self):
        return self.queryset.filter(cart__merchant=self.request.user.merchant)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.cart.merchant != request.user.merchant:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.cart.merchant != request.user.merchant:
            return Response({"error": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)