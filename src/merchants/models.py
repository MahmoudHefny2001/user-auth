from django.db import models


from users.models import User

from .managers import MerchantManager


class MerchantBridge(User):
    """
    This is a proxy model for the User model.
    It is used to create a separate table for the Merchant model.
    This table will not be created on the postgres database tables.
    Instead, it will be used on the Merchant table as a 'bridge - connector - pointer' to the users model.
    """
    base_role = User.Role.MERCHANT

    class Meta:
        proxy = True

    objects = MerchantManager()    # Custom Manager for the Merchant model used only to filter the admins.




class Merchant(MerchantBridge):
    """
    This is the Merchant model.
    It is used to create an Merchant instance.
    """
    

    address = models.TextField(blank=True, null=True)


    class Meta:
        db_table = "merchants"
        


class MerchantProfile(models.Model):
    """
    This is the MerchantProfile model.
    It is used to create an MerchantProfile instance.
    """
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE, related_name='profile')
    

    image = models.ImageField(upload_to='images/merchant/profiles/', blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    merchant_zip_code = models.CharField(max_length=100, blank=True, null=True)



    class Meta:
        db_table = "merchants_profiles"
        verbose_name = "Merchant Profile"
        verbose_name_plural = "Merchant Profiles"

    
    def __str__(self):
        return self.merchant.full_name