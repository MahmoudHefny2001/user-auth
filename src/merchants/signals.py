from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Merchant, MerchantProfile


@receiver(post_save, sender=Merchant)
def create_merchant_profile(sender, instance, created, **kwargs):
    try:
        if created and instance.role == "MERCHANT":
            merchant_profile = MerchantProfile.objects.create(merchant=instance)
            merchant_profile.save()
    except Exception as e:
        print(e)