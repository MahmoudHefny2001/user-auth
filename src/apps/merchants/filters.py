import django_filters

from .models import Merchant, MerchantProfile


class MerchantFilter(django_filters.FilterSet):
    class Meta:
        model = Merchant
        fields = {
            'full_name': ['icontains', 'exact'],
            'address': ['icontains', 'exact'],
            'payment_information': ['icontains', 'exact'],
        }



class MerchantProfileFilter(django_filters.FilterSet):
    class Meta:
        model = MerchantProfile
        fields = {
            'tax_id': ['icontains', 'exact'],
            'about_us': ['icontains', 'exact'],
            'twitter_url': ['icontains', 'exact'],
            'website_url': ['icontains', 'exact'],
            'facebook_url': ['icontains', 'exact'],
            'linkedin_url': ['icontains', 'exact'],
            'return_policy': ['icontains', 'exact'],
            'instagram_url': ['icontains', 'exact'],
            'shipping_address': ['icontains', 'exact'],
            'shipping_options': ['icontains', 'exact'],
            'merchant_zip_code': ['icontains', 'exact'],
        }