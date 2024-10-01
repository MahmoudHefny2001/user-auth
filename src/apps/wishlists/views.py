from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import Wishlist, WishlistItem

from .serializers import WishListItemSerializer

from apps.products.models import Product

from apps.customers.models import Customer

from apps.users.customJWT import CustomJWTAuthenticationClass


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.filter()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomJWTAuthenticationClass, JWTAuthentication,]
    serializer_class = WishListItemSerializer

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    http_method_names   = ['get','delete', 'post',]
    
    def get_queryset(self):
        customer = None
        try:
            customer = self.request.user.customer
        except AttributeError:
            return self.queryset.none()
            
        if customer:
            return self.queryset.filter(wishlist__customer=customer)
    

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

        # Check if the user adding the product to the wishlist didn't add it before
        if WishlistItem.objects.filter(wishlist__customer=customer, product=product).exists():
            return Response(
                {
                    "message": "Product already added to wishlist.",
                    
                },
                status=400
            )

        if product and customer:
            # if customer has no wishlist create it else retreive it then add items to wishlistitmes
            if Wishlist.objects.filter(customer=customer).exists():
                wishlist = Wishlist.objects.get(customer=customer)
                wishlist_product = WishlistItem.objects.create(wishlist=wishlist, product=product)
                wishlist.save()
                wishlist_product.save()
            else:
                wishlist = Wishlist.objects.create(customer=customer)
                wishlist_product = WishlistItem.objects.create(wishlist=wishlist, product=product)
                wishlist.save()
                wishlist_product.save()
    
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

        if not WishlistItem.objects.filter(wishlist__customer=customer, product=product).exists():
            return Response(
                {
                    "message": "Product not found in wishlist.",
                    
                },
                status=400
            )

        if product and customer:
            wishlist = Wishlist.objects.get(customer=customer)
            wishlist_product = WishlistItem.objects.get(wishlist=wishlist, product=product)
            wishlist_product.delete()
            wishlist.save()

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
        