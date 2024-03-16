from rest_framework import viewsets, views
from .models import Product, Category, ProductAttachment
from .serializers import GetProductsSerializer, RetrieveProductsSerializer, GetProductsSerializerForMerchants, RetrieveProductsSerializerForMerchants

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import ProductFilter

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from users.customJWT import CustomJWTAuthenticationClass

from rest_framework.permissions import IsAuthenticated

# from .permissions import IsMerchant


class HomeViewSet(views.APIView):
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    permission_classes = [AllowAny]
    

    def get(self, request, *args, **kwargs):

        products = []

        for product in Product.objects.order_by('category').distinct('category')[:5]:

            product_data = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "on_sale": product.on_sale,
                "colors": product.colors,
                "sale_percent": str(int(product.sale_percent)) + "%",
                "price_after_sale": product.price_after_sale ,
                "main_image": product.get_image_url(),
                "average_rating": product.average_rating,
            }
            products.append(product_data)
    

        # select only name from the category
        categories = Category.objects.all().values('name')[:5]

        return Response(
            {
                "categories": list(categories), 
                "products": list(products),
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
    


class ProductViewSetForMerchants(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [
        IsAuthenticated, 
        # IsMerchant,
        ]
    authentication_classes = [CustomJWTAuthenticationClass, JWTAuthentication,]

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    http_method_names   = ['get', 'retrieve', 'post', 'put', 'patch', 'delete']

    filterset_class = ProductFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'name', 'category']

    
    def get_queryset(self):
        
        return Product.objects.filter(merchant=self.request.user).order_by('-created')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GetProductsSerializerForMerchants
        else:
            return RetrieveProductsSerializerForMerchants
    

    def create(self, request, *args, **kwargs):
        try:
            product = Product.objects.create(
                merchant=request.user.merchant,
                name=request.data.get('name'),
                description=request.data.get('description'),
                price=request.data.get('price'),
                quantity=request.data.get('quantity'),
                category_id=request.data.get('category_id'),
                colors=request.data.get('colors'),
                on_sale=request.data.get('on_sale'),
                sale_percent=request.data.get('sale_percent'),
                image=request.data.get('image'),
            )
            product.save()
            return Response(
                {
                    "message": "Product created successfully.",
                    "product": RetrieveProductsSerializer(product).data,
                }, 
                status=201
            )
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)
    

    def partial_update(self, request, *args, **kwargs):
        product = self.get_object()
        
        if product.merchant != request.user.merchant:
            return Response(
                {
                    "error": "You are not allowed to update this product."
                },
                status=403
            )
        
        try:
            name = request.data.get('name', None)
            description = request.data.get('description', None)
            price = request.data.get('price', None)
            quantity = request.data.get('quantity', None)
            colors = request.data.get('colors', None)
            on_sale = request.data.get('on_sale', None)
            sale_percent = request.data.get('sale_percent', None)
            image = request.data.get('image', None)


            if name:
                product.name = name
            if description:
                product.description = description
            if price:
                product.price = price
            if quantity:
                product.quantity = quantity
        
            # Split colors string into a list of strings
            if colors is not None:
                import re

                # Regular expression pattern to split by spaces, commas, and hyphens
                delimiter_pattern = re.compile(r'[,\s-]+')

                # Split the colors string using the regular expression pattern
                colors = delimiter_pattern.split(colors)
                
                if isinstance(colors, str):
                    # Split the string using the regular expression pattern
                    colors = delimiter_pattern.split(colors)
                    # Remove empty strings from the list (if any)
                    colors = [color.strip() for color in colors if color.strip()]
                elif isinstance(colors, list):
                    # Remove leading and trailing whitespace from each color
                    colors = [color.strip() for color in colors]

                product.colors = colors
            
            if on_sale:
                product.on_sale = on_sale
            if sale_percent:
                product.sale_percent = sale_percent
            if image:
                product.image = image
            

            # Handle product attachmetns update like adding multiple images
            # Multiple images can be added to a product
            attachments = request.FILES.getlist('attachments', None)


            if attachments:
                for attachment in attachments:
                    product_attachment = ProductAttachment.objects.create(
                        product=product,
                        attachment=attachment
                    )
                    product_attachment.save()

            product.save()

            return Response(
                {
                    "message": "Product updated successfully.",
                    "product": RetrieveProductsSerializer(product).data,
                }, 
                status=200
            )
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)
