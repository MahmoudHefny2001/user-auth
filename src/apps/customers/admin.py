from django.contrib import admin

from .models import Customer, CustomerProfile


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'address',]
    search_fields = ['full_name', 'email', 'phone_number', 'address']
    
    # Exclude fields from the admin form like password, last_login, is_superuser, is_staff, is_active, date_joined
    exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions', 'role']



class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['customer', 'birth_date', 'bio']
    search_fields = ['customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address']
    list_filter = ['birth_date', 'bio', 'customer__full_name', 'customer__email', 'customer__phone_number', 'customer__address']
    


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
