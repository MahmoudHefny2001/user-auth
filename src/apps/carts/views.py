from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem

from apps.products.models import Product

from apps.customers.models import Customer

from apps.users.customJWT import CustomJWTAuthenticationClass


class CartViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomJWTAuthenticationClass, JWTAuthentication,]
    serializer_class = CartItemSerializer

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    http_method_names   = ['get','delete', 'post', 'patch', 'put']
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__customer=self.request.user.customer)


    def create(self, request, *args, **kwargs):

        if not request.data.get("product_id"):
            return Response({"error": "Product ID is required"}, status=400)


        product = Product.objects.get(id=request.data.get("product_id"))
        
        cart = Cart.objects.filter(customer=request.user.customer).first()

        quantity = request.data.get("quantity", 1)

        # if the product is already in the cart, return an error
        if cart and CartItem.objects.filter(cart=cart, product=product).exists():
            return Response({"error": "Product already in cart"}, status=400)

        if not cart:
            cart = Cart.objects.create(customer=request.user.customer)
        
        
        cart_item = CartItem.objects.create(cart=cart, product=product, item_quantity=quantity)

        serializer = CartItemSerializer(cart_item)

        return Response(serializer.data)

    

    def list(self, request, *args, **kwargs):
        cart = Cart.objects.filter(customer=request.user.customer).first()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    

    
    def partial_update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        quantity = request.data.get("quantity", 1)
        cart_item.item_quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
    