from rest_framework import viewsets, views
from .models import Product, Category
from .serializers import GetProductsSerializer, RetrieveProductsSerializer

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import ProductFilter

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle



class HomeViewSet(views.APIView):
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    permission_classes = [AllowAny]
    
    products = []

    for product in Product.objects.order_by('category').distinct('category')[:5]:

        product_data = {
            "id": product.id,
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

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]


    http_method_names   = ['get', 'retrieve']

    filterset_class = ProductFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'name', 'category']

    
    def get_serializer_class(self):
        if self.action == 'list':
            return GetProductsSerializer
        else:
            return RetrieveProductsSerializer
    
