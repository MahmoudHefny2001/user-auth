from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.products.models import Product
from .models import Order, OrderItem

from time import sleep

@receiver(post_save, sender=Product)
def cancel_order_when_product_is_deleted(sender, instance, created, **kwargs):
    try:
        sleep(5)
        orders = Order.objects.filter(cart__product=instance)
        for order in orders:
            order.status = "CANCELLED"
            order.save()
    except Exception as e:
        print(e)



# @receiver(post_save, sender=Order)
# def delete_cart_items_after_order_is_created(sender, instance, created, **kwargs):
#     if created:
#         instance.cart.delete()
        # 