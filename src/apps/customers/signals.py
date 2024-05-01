from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer, CustomerProfile


@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance, created, **kwargs):
    try:
        if created and instance.role == "CUSTOMER":
            customer_profile = CustomerProfile.objects.create(customer=instance)
            customer_profile.save()
    except Exception as e:
        print(e)