from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import Whishlist


from .serializers import WhishListSerializer

from products.models import Product

from customers.models import Customer

class WhishList(viewsets.ModelViewSet):
    queryset = Whishlist.objects.filter()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]


    http_method_names   = ['get','delete', 'post',]
    
    def get_queryset(self):
        return Whishlist.objects.filter(customer=self.request.user.customer)
    
    def get_serializer_class(self):
        return WhishListSerializer
        
        

    def create(self, request, *args, **kwargs):
        
        product = Product.objects.get(id=request.data.get('product_id'))
        customer = Customer.objects.get(id=request.user.customer.id)

        if product and customer:
            whishlist_product = Whishlist.objects.create(customer=customer, product=product)
            whishlist_product.save()
            return Response(
                {
                    "message": "Product added to favourites successfully.",
                    
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
        product = Product.objects.get(id=request.data.get('product_id'))
        customer = Customer.objects.get(id=request.user.customer.id)

        if product and customer:
            whishlist_product = Whishlist.objects.get(customer=customer, product=product)
            whishlist_product.delete()
            return Response(
                {
                    "message": "Product removed from favourites successfully.",
                    
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