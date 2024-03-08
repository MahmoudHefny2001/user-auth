from rest_framework import viewsets, generics, views
from .models import Product, Category, ProductReport, ProductReview, ProductAttachment, ProductAttachment
from .serializers import GetProductsSerializer, CategorySerializer, RetrieveProductsSerializer, GetFavouriteProductsSerializer

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import ProductFilter

from customers.models import CustomerFavouriteProduct

from rest_framework.permissions import IsAuthenticated


class HomeViewSet(views.APIView):
    
    permission_classes = [AllowAny]
    
    products = []

    for product in Product.objects.order_by('category').distinct('category')[:5]:

        product_data = {
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "on_sale": product.on_sale,
            "sale_percent": str(int(product.sale_percent)) + "%",
            "price_after_sale": product.price_after_sale ,
            "main_image": product.get_image_url(),
        }
        products.append(product_data)
    

    # select only name from the category
    categories = Category.objects.all().values('name')[:5]


    def get(self, request, *args, **kwargs):

        return Response(
            {
                "categories": list(self.categories), 
                "products": list(self.products),
            }
        )

    


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    # serializer_class = GetProductsSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication,]

    http_method_names   = ['get', 'retrieve']

    filterset_class = ProductFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'name', 'category']

    
    def get_serializer_class(self):
        if self.action == 'list':
            return GetProductsSerializer
        else:
            return RetrieveProductsSerializer
    


class AddToFavourites(views.APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if product_id:
            product = Product.objects.get(id=product_id)
            favourite_product = CustomerFavouriteProduct.objects.create(customer=request.user.customer, product=product)
            favourite_product.save()
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
        product_id = kwargs.get('product_id', None)
        if product_id:
            product = Product.objects.get(id=product_id)
            favourite_product = CustomerFavouriteProduct.objects.get(customer=request.user.customer, product=product)
            favourite_product.delete()
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



class FavouriteProducts(viewsets.ModelViewSet):
    queryset = CustomerFavouriteProduct.objects.filter()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]

    http_method_names   = ['get','delete', 'post',]
    
    def get_queryset(self):
        return CustomerFavouriteProduct.objects.filter(customer=self.request.user.customer)
    
    def get_serializer_class(self):
        return GetFavouriteProductsSerializer
        
        

    def post(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id', None)
        if product_id:
            product = Product.objects.get(id=product_id)
            favourite_product = CustomerFavouriteProduct.objects.create(customer=request.user.customer, product=product)
            favourite_product.save()
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
        product_id = kwargs.get('product_id', None)
        if product_id:
            product = Product.objects.get(id=product_id)
            favourite_product = CustomerFavouriteProduct.objects.get(customer=request.user.customer, product=product)
            favourite_product.delete()
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