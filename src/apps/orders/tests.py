
from django.test import TestCase
from rest_framework.test import APIClient

from apps.merchants.models import Merchant
from apps.products.models import Product
from apps.customers.models import Customer
from apps.carts.models import Cart, CartItem
from apps.orders.models import Order, OrderItem

from django.db.utils import OperationalError

import threading

from time import sleep

from django.db import transaction

import random


class TestAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
    
        for i in range(5):
            merchant_data = {
                "email": f"merchant{i}@mail.com",
                "full_name": f"Merchant {i}",
                "password": "passwordMm-123456",
                "phone_number": f"{i}235678901",
                "address": f"1234 Main St {i}",
                "payment_information": "Cash",
                "terms_agreement": True,
            }

            with transaction.atomic():
                merchant = Merchant.objects.create_merchant(**merchant_data)
                merchant.save()

        print("MERCHANT Created Successfully")


        for i in range(5):
            customer_data = {
                "full_name": f"Customer {i}",
                "email": f"customer{i}@mail.com",
                "password": "passwordMm-123456",
                "phone_number": f"{i}5345678901",
            }
            with transaction.atomic():
                Customer.objects.create(**customer_data)    
        

        print("CUSTOMERS-------------->",)



        product_data = {
            "name": "new new Unique Product 222",
            "description": "new new Unique Description sss",
            "price": 100000,
            "quantity": 50,
            "tag": "smart phones",
            "merchant_id": 1  # Assuming merchant ID is 1
        }


        with transaction.atomic():
            product = Product.objects.create(**product_data)
            product.save()
        

        print("PRODUCT Created Successfully", product)    




    def create_cart(self):
        for customer in Customer.objects.all():
            if not Cart.objects.filter(customer=customer).exists():
                with transaction.atomic():
                    cart = Cart.objects.create(customer=customer)
                    cart.save()
                print("CART-------------->: ", cart)
    


    def create_cart_item(self):
        for cart in Cart.objects.all():

            product = Product.objects.filter(available=True).first()

            random_quantity = random.randint(1, 4)

            if CartItem.objects.filter(cart=cart, product=product).exists(): 
                return
            else:
                with transaction.atomic():
                    cart_item = CartItem.objects.create(cart=cart, product=product, item_quantity=random_quantity)
                    cart_item.save()
                print("CART ITEMS------------>", cart_item)
        
        print("CART ITEMS-------------->",)

    

    def create_order(self):
        try:
            with transaction.atomic():
        
                for customer in Customer.objects.all():
                    # Create the order
                    order = Order.objects.create(
                        customer=customer,
                        shipping_address="1234 Main St",
                    )

                    order.save()

                    print("ORDER CREATED-------------->\n", order)


                    try:
                        self.create_cart()
                    except Exception as e:
                        print(e)
                        return None

                    try:
                        self.create_cart_item()
                    except Exception as e:
                        print(e) 
                        return None

                    # Create order items
                    order_items = []
                    total_price = 0  # Initialize total_price

                    cart = Cart.objects.get(customer=customer)

                    for cart_item in cart.cart_items.all():
                        sub_total_price = cart_item.get_sub_total()  # Calculate sub_total_price
                        total_price += sub_total_price  # Add to total_price
                        if cart_item.item_quantity > cart_item.product.quantity:
                            raise Exception("Product quantity is not enough to fulfill the order")
                        try:
                            order_items.append(OrderItem(
                                order=order,  # Set the order attribute
                                product=cart_item.product,
                                quantity=cart_item.item_quantity,
                                sub_total_price=sub_total_price
                            ))
                        except Exception as e:
                            print(e)
                            return None

                    # Bulk create OrderItems
                    OrderItem.objects.bulk_create(order_items)

                    # Set the total_price for the order
                    order.total_price = total_price
                    order.save()

                    print("ORDER CREATED-------------->\n", order)

                    # Clear the cart after the order is created
                    cart_items = CartItem.objects.filter(cart=cart)
                    for cart_item in cart_items:
                        cart_item.delete()
                    cart.delete()

                    # Update product quantity and availability
                    for order_item in order.order_items.all():
                        product = order_item.product
                        product.quantity -= order_item.quantity
                        if product.quantity <= 0:
                            product.available = False
                        product.save()
                    
                    print("PRODUCT UPDATED-------------->\n", product)
            
        except Exception as e:
            print(e)
            raise e
            

    
    def test_concurrent_create_order(self):
        try:
            # run concurrent create order
            threads = []
            for i in range(5):
                thread = threading.Thread(target=self.create_order)
                threads.append(thread)
            

            try:
                for thread in threads:
                    thread.start()
                    sleep(1)
            except OperationalError as e:
                print(e)
                print("Cannot create order at this time. Please try again later.")
                sleep(5)
                # redo the operation
                for thread in threads:
                    thread.start()
                    sleep(1)
            

            try:
                for thread in threads:
                    thread.join()
                    print("Thread joined")
                    print("Thread finished")
            except OperationalError as e:
                print(e)
                print("Cannot create order at this time. Please try again later.")
                sleep(5)
                # redo the operation
                for thread in threads:
                    thread.start()
                    sleep(1)


        except Exception as e:
            print(e)
            print("Cannot create order at this time. Please try again later.")


        try:
            i = 0
            while i < 5:

                print("\nTEST CONCURRENT CREATE ORDER-------------->")

                print("Product Before Order Creation: ")
                # print all data of the product before order creation
                for key, value in Product.objects.first().__dict__.items():
                    if key in ["id", "name", "quantity", "available", "merchant_id", "tag", "average_rating", "price", "price_after_sale", "on_sale", "sale_percent", "category_id", "image", "description", "bar_code"]:
                        print(f"{key}: {value}")

                print("\nTEST CONCURRENT CREATE ORDER-------------->")

                try:
                    self.create_order()
                except Exception as e:
                    print(e)
                    return None
                

                print("\nOrder Details: ")
                for key, value in Order.objects.first().__dict__.items():
                    if key in ["id", "cart_id", "shipping_address", "order_status",]:
                        print(f"{key}: {value}")

                print("\nProduct After Order Creation: ")
                # print all data of the product after order creation
                for key, value in Product.objects.first().__dict__.items():
                    if key in ["id", "name", "quantity", "available", "merchant_id", "tag", "average_rating", "price", "price_after_sale", "on_sale", "sale_percent", "category_id", "image", "description", "bar_code"]:
                        print(f"{key}: {value}")

                i += 1

        except Exception as e:
            print(e)
            print("Cannot create order at this time. Please try again later.")
        

