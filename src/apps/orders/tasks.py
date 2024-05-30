from celery import shared_task
from django.db import transaction


from .models import OrderItem

from apps.carts.models import CartItem

from django.db import transaction, DatabaseError

import time



# import django db handler for concurrent transactions
from django.db import transaction, DatabaseError


# make the update of the product quantity and availability in the database within a transaction and without blocking the main thread
# @transaction.atomic
# @shared_task
# def update_product_quantity_and_availability(order):
#     # handle db locks on the product rows
#     try:
#         with transaction.atomic():
            
#             for order_item in OrderItem.objects.filter(order=order):
#                 product = order_item.product
#                 product.quantity -= order_item.quantity
#                 if product.quantity <= 0:
#                     product.available = False
#                 product.save()
#     except DatabaseError as e:
#         print(f'Failed to update product quantity and availability for order {order.id} after many attempts')
#     except Exception as e:
#         raise e
    


MAX_RETRIES = 5
DELAY_BETWEEN_RETRIES = 10  # seconds

@shared_task
def update_product_quantity_and_availability(order):
    for attempt in range(MAX_RETRIES):
        try:
            with transaction.atomic():
                # Fetch order items for the given order and lock the associated product rows
                order_items = OrderItem.objects.select_related('product').filter(order_id=order.id).select_for_update()
                for order_item in order_items:
                    product = order_item.product
                    product.quantity -= order_item.quantity
                    if product.quantity <= 0:
                        product.available = False
                    product.save()
            break  # Exit loop if successful
        except DatabaseError as e:
            if attempt < MAX_RETRIES:
                time.sleep(DELAY_BETWEEN_RETRIES)
                update_product_quantity_and_availability(order=order)
            else:
                print(f'Failed to update product quantity and availability for order {order.id} after {MAX_RETRIES} attempts')
                print("Cannot Create Order at this time. Please try again later.")
                # Raise the original exception after all retries
                raise e



# Clear the cart after the order is created within a transaction and without blocking the main thread
@transaction.atomic
@shared_task
def clear_cart(cart):
    try:
        with transaction.atomic():
            # Clear the cart after the order is created
            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                cart_item.delete()
            cart.delete()
    except Exception as e:
        raise e
    