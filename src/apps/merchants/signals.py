from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Merchant, MerchantProfile


@receiver(post_save, sender=Merchant)
def create_merchant_profile(sender, instance, **kwargs):
    """
    This method creates a merchant profile for the merchant.
    """
    if kwargs["created"]:
        MerchantProfile.objects.create(merchant=instance)
        