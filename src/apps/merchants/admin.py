from collections.abc import Sequence
from django.contrib import admin
from django.http import HttpRequest


from .models import Merchant, MerchantProfile


class MerchantAdmin(admin.ModelAdmin):
    
    def business_name(self, obj):
        return obj.full_name

    business_name.short_description = 'Business Name'

    list_display = ['business_name', 'email', 'phone_number', 'address',]
    
    search_fields = ['full_name', 'email', 'phone_number', 'address', ]
    # Exclude fields from the admin form like password, last_login, is_superuser, is_staff, is_active, date_joined
    exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions', 'role']

    # display the full_name of the merchant in the create page as business_name
    def get_form(self, request: HttpRequest, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['full_name'].label = 'Business Name'
        return form
    
        

class MerchantProfileAdmin(admin.ModelAdmin):

    def business_name(self, obj):
        return obj.merchant.full_name

    business_name.short_description = 'Business Name'

    
    list_display = ['merchant', 'merchant_zip_code', 'tax_id', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'shipping_address', 'shipping_options', 'about_us', 'return_policy', ]
    
    search_fields = ['merchant__full_name', 'merchant__email', 'merchant__phone_number', 'merchant__address']

    list_filter = ['merchant__full_name', 'merchant__email', 'merchant__phone_number', 'merchant__address']
    



admin.site.register(Merchant, MerchantAdmin)
admin.site.register(MerchantProfile, MerchantProfileAdmin)