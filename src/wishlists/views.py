from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import Wishlist

from .serializers import WishListSerializer

from products.models import Product

from customers.models import Customer

from users.customJWT import CustomJWTAuthenticationClass


class WishListViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.filter()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomJWTAuthenticationClass, JWTAuthentication,]
    serializer_class = WishListSerializer

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]


    http_method_names   = ['get','delete', 'post',]
    
    def get_queryset(self):
        return Wishlist.objects.filter(customer=self.request.user.customer)
    

    def create(self, request, *args, **kwargs):
        
        product = Product.objects.get(id=request.data.get('product_id'))
        customer = Customer.objects.get(id=request.user.customer.id)

        # Check if the user adding the product to the wishlist didn't add it before
        if Wishlist.objects.filter(customer=customer, product=product).exists():
            return Response(
                {
                    "message": "Product already added to wishlist.",
                    
                },
                status=400
            )

        if product and customer:
            whishlist_product = Wishlist.objects.create(customer=customer, product=product)
            whishlist_product.save()
            return Response(
                {
                    "message": "Product added to wishlist successfully.",
                    
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
        We can delete from the wishlist by sending the product id in the request body.
        Also we can delete from wishlist by sending the wishlist object id itself but here we go along with the product id.
        """


        product = Product.objects.get(id=request.data.get('product_id'))
        customer = Customer.objects.get(id=request.user.customer.id)

        if not Wishlist.objects.filter(customer=customer, product=product).exists():
            return Response(
                {
                    "message": "Product not found in wishlist.",
                    
                },
                status=400
            )

        if product and customer:
            whishlist_product = Wishlist.objects.get(customer=customer, product=product)
            whishlist_product.delete()
            return Response(
                {
                    "message": "Product removed from wishlist successfully.",
                    
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