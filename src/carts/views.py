from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .serializers import CartSerializer
from .models import Cart

from products.models import Product

from customers.models import Customer

from users.customJWT import CustomJWTAuthenticationClass


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomJWTAuthenticationClass, JWTAuthentication,]
    serializer_class = CartSerializer

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]


    http_method_names   = ['get','delete', 'post',]
    
    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user.customer)
        
    def create(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=request.data.get('product_id'))
            customer = Customer.objects.get(id=request.user.customer.id)

        except Product.DoesNotExist:
            return Response(
                {
                    "message": "Product not found.",
                },
                status=400
            )

        # Check if the user adding the product to the cart didn't add it before
        if Cart.objects.filter(customer=customer, product=product).exists():
            return Response(
                {
                    "message": "Product already added to cart.",
                    
                },
                status=400
            )

        if product and customer:
            cart_product = Cart.objects.create(customer=customer, product=product)
            cart_product.save()
            return Response(
                {
                    "message": "Product added to cart successfully.",
                    
                },
                status=201
            )
        else:
            return Response(
                {
                    "message": "Product id is required."
                },
                status=400
            )
        

    def delete(self, request, *args, **kwargs):

        """
        We can delete from the cart by sending the product id in the request body.
        Also we can delete from cart by sending the cart object id itself but here we go along with the product id.
        """

        try:

            product = Product.objects.get(id=request.data.get('product_id'))
            customer = Customer.objects.get(id=request.user.customer.id)
        
        except Product.DoesNotExist:
            return Response(
                {
                    "message": "Product not found.",
                },
                status=400
            )

        if not Cart.objects.filter(customer=customer, product=product).exists():
            return Response(
                {
                    "message": "Product not found in cart.",
                    
                },
                status=400
            )

        if product and customer:
            cart_product = Cart.objects.get(customer=customer, product=product)
            cart_product.delete()
            return Response(
                {
                    "message": "Product removed from cart successfully.",
                    
                },
                status=200
            )
        else:
            return Response(
                {
                    "message": "Product id is required."
                },
                status=400
            )
