from rest_framework import viewsets, generics, views
from .models import Product, Category, ProductReport, ProductReview, ProductAttachment
from .serializers import ProductSerializer, CategorySerializer

from rest_framework.permissions import AllowAny

from rest_framework.response import Response


class HomeViewSet(views.APIView):
    
    permission_classes = [AllowAny]
    
    # products = Product.objects.order_by('category').distinct('category').values('name', 'description', 'price', 'image')[:5]


    products_with_attachments = []

    for product in Product.objects.order_by('category').distinct('category')[:5]:
        attachments = ProductAttachment.objects.filter(product=product).values_list('attachment', flat=True)[:3]
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "main_image": str(product.image),
            "images": list(attachments),
        }
        products_with_attachments.append(product_data)
    

    # select only name and description from the category
    categories = Category.objects.all().values('name')[:5]


    def get(self, request):
        return Response(
            {
                "categories": list(self.categories), 
                "products": list(self.products_with_attachments),
            }
        )

    
    


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer