from django.db import models


from apps.users.models import User

from .managers import CustomerManager


class CustomerBridge(User):
    """
    This is a proxy model for the User model.
    It is used to create a separate table for the Customer model.
    This table will not be created on the postgres database tables.
    Instead, it will be used on the customers table as a 'bridge - connector - pointer' to the users model.
    """
    base_role = User.Role.CUSTOMER

    class Meta:
        proxy = True

    objects = CustomerManager()    # Custom Manager for the Customer model used only to filter the admins.




class Customer(CustomerBridge):
    """
    This is the Customer model.
    It is used to create an Customer instance.
    """
    

    address = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "customers"
        


class CustomerProfile(models.Model):
    """
    This is the CustomerProfile model.
    It is used to create an CustomerProfile instance.
    """
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='profile')
    
    birth_date = models.DateField(blank=True, null=True)

    image = models.ImageField(upload_to='images/customers/profiles/', blank=True, null=True, default='media/images/customers/profiles/blank_p71odd.jpg')

    bio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "customer_profiles"
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"


    def __str__(self):
        return f"{self.customer.full_name} Profile"
    
    # account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # points = models.PositiveIntegerField(default=0)
    # is_active = models.BooleanField(default=True)
    # is_verified = models.BooleanField(default=False)
    # is_blocked = models.BooleanField(default=False)