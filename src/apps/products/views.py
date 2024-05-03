from rest_framework import viewsets, views
from .models import Product, Category, ProductAttachment
from .serializers import GetProductsSerializer, RetrieveProductsSerializer, GetProductsSerializerForMerchants, RetrieveProductsSerializerForMerchants, CategorySerializer

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import ProductFilter

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from apps.users.customJWT import CustomJWTAuthenticationClass

from rest_framework.permissions import IsAuthenticated

# from .permissions import IsMerchant



class CategoryViewSet(views.APIView):

    """
    Category ViewSet this is used to get all categories
    """

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    def get(self, request, *args, **kwargs):

        categories = Category.objects.all()
        return Response(
            {
                # RETURN THE NAME AND ID OF THE CATEGORY ONLY NOT THE DESCRIPTION
                "categories": list(categories.values('name', 'id'))
                # "categories": CategorySerializer(categories, many=True).data
            }
        )





class HomeViewSet(views.APIView):


    """
    Home ViewSet this is used to get the top 5 categories and products
    """
    
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
                "sale_percent": str(int(product.sale_percent)) + "%",
                "price_after_sale": product.price_after_sale ,
                "main_image": product.get_image_url(),
                "average_rating": product.average_rating,
            }
            products.append(product_data)

            # add colors to the product data
            for product in products:
                from .models import ProductColor
                from .serializers import ProductColorSerializer
                product['colors'] = ProductColorSerializer(ProductColor.objects.filter(product=product['id']), many=True).data

        # select only name from the category
        categories = Category.objects.all().values('name')[:5]

        return Response(
            {
                "categories": list(categories), 
                "products": list(products),
            }
        )

    


class ProductViewSet(viewsets.ModelViewSet):

    """
    Product ViewSet this is used to get all products and retrieve a single product
    """


    queryset = Product.objects.filter(available=True).order_by('-created')
    # serializer_class = GetProductsSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication,]

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]


    http_method_names   = ['get', 'retrieve']

    filterset_class = ProductFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'name', 'category']

    
    def get_serializer_class(self):
        """
        This method returns a serializer class based on the action.
        if the REQUEST is list /(GET all products)/ it returns GetProductsSerializer FOR LISTING ALL PRODUCTS
        if the REQUEST is retrieve /(GET single product)/ it returns RetrieveProductsSerializer FOR RETRIEVING A SINGLE PRODUCT
        """
        if self.action == 'list':
            return GetProductsSerializer
        else:
            return RetrieveProductsSerializer
    


class ProductViewSetForMerchants(viewsets.ModelViewSet):
    
    """
    Product ViewSet for Merchants.
    """


    queryset = Product.objects.all()
    permission_classes = [
        IsAuthenticated, 
        # IsMerchant,
        ]
    authentication_classes = [CustomJWTAuthenticationClass, JWTAuthentication,]

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    http_method_names   = ['get', 'retrieve', 'post', 'patch', 'delete']

    filterset_class = ProductFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'name', 'category']

    
    def get_queryset(self):
        """
        This view should return a list of all the products that belong to the currently authenticated merchant.
        """
        return Product.objects.filter(merchant=self.request.user).order_by('-created')
    
    def get_serializer_class(self):
        """
        This method returns a serializer class based on the action.
        if the REQUEST is list /(GET all products)/ it returns GetProductsSerializerForMerchants FOR LISTING ALL PRODUCTS
        if the REQUEST is retrieve /(GET single product)/ it returns RetrieveProductsSerializerForMerchants FOR RETRIEVING A SINGLE PRODUCT
        """
        if self.action == 'list':
            return GetProductsSerializerForMerchants
        else:
            return RetrieveProductsSerializerForMerchants
    

    def create(self, request, *args, **kwargs):
        """
        This method is used to create a product for the currently authenticated merchant.
        """


        try:
            
            try:
                product = Product.objects.create(
                    bar_code=request.data.get('bar_code',),
                    merchant=request.user.merchant,
                    name=request.data.get('name'),
                    description=request.data.get('description'),
                    price=request.data.get('price'),
                    quantity=request.data.get('quantity'),
                    category_id=request.data.get('category_id', None),
                    on_sale=request.data.get('on_sale', None),
                    sale_percent=request.data.get('sale_percent', None),
                    image=request.data.get('image',),
                )
            except Exception as e:
                return Response({"error": str(e)}, status=400)

            # colors=request.data.getlist('colors', None),
            # if colors is not None and len(colors) > 0:
                
            #     from .models import ProductColor
            #     for color in colors:
            #         product_color = ProductColor.objects.create(
            #             product=product,
            #             color=color
            #         )
            #         product_color.save()
            
            # Handle product attachmetns creation like adding multiple images
            attachments = request.FILES.getlist('attachments', None)

            if attachments:
                for attachment in attachments:
                    product_attachment = ProductAttachment.objects.create(
                        product=product,
                        attachment=attachment
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

        """
        This method is used to update a product for the currently authenticated merchant.
        """

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
            on_sale = request.data.get('on_sale', None)
            sale_percent = request.data.get('sale_percent', None)
            image = request.data.get('image', None)

            colors = request.data.get('colors', None)

            if name:
                product.name = name
            if description:
                product.description = description
            if price:
                product.price = price
            if quantity:
                product.quantity = quantity
        
            # if colors:
                # from .models import ProductColor
                # Delete all colors for the product
                # ProductColor.objects.filter(product=product).delete()
                # for color in colors:
                    # product_color = ProductColor.objects.create(
                        # product=product,
                        # color=color
                    # )
            
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



    def destroy(self, request, *args, **kwargs):
        """
        This method is used to delete a product for the currently authenticated merchant.
        """
        
        product = self.get_object()
        if product.merchant != request.user.merchant:
            return Response(
                {
                    "error": "You are not allowed to delete this product."
                },
                status=403
            )
        
        return super().destroy(request, *args, **kwargs)
    
