import django_filters
from .models import Product, Category


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'name' : ['icontains','exact'],
            'description' : ['icontains', 'exact'],
            }
    


class ProductFilter(django_filters.FilterSet):
    # Here we filter Product items according to their category name
    category = django_filters.CharFilter(field_name="category__name", lookup_expr="iexact")
    
    # description = django_filters.CharFilter(field_name='description', lookup_expr='contains')
    # available = django_filters.BooleanFilter(field_name='available')
   
    class Meta:
        model = Product
        fields = {
            'name' : ['icontains','exact'],
            'description' : ['icontains', 'exact'],
            'price' : ['gte', 'lte'],
            }