from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.products.models import Product
from .models import Order, OrderItem


@receiver(post_save, sender=Product)
def cancel_order_when_product_is_deleted(sender, instance, created, **kwargs):
    try:
        orders = Order.objects.filter(cart__product=instance)
        for order in orders:
            order.status = "CANCELLED"
            order.save()
    except Exception as e:
        print(e)
