from celery import shared_task
from django.db import transaction


from .models import OrderItem

from apps.carts.models import CartItem

# make the update of the product quantity and availability in the database within a transaction and without blocking the main thread
@transaction.atomic
@shared_task
def update_product_quantity_and_availability(order):
    try:
        # Update the product quantity and availability
        for order_item in OrderItem.objects.filter(order=order):
            product = order_item.product
            product.quantity -= order_item.quantity
            if product.quantity <= 0:
                product.available = False
            product.save()
    except Exception as e:
        raise e



# Clear the cart after the order is created within a transaction and without blocking the main thread
@transaction.atomic
@shared_task
def clear_cart(cart):
    try:
        # Clear the cart after the order is created
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            cart_item.delete()
        cart.delete()
    except Exception as e:
        raise e
    