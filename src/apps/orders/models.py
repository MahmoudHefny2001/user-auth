from django.db import models

from django_extensions.db.models import TimeStampedModel

from django.core.validators import MinValueValidator, MaxValueValidator

from apps.customers.models import Customer

from apps.products.models import Product

from apps.carts.models import Cart


class Order(TimeStampedModel):
    
    class OrderStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        PROCESSING = 'Processing', 'Processing'
        SHIPPED = 'Shipped', 'Shipped'
        DELIVERED = 'Delivered', 'Delivered'
        CANCELED = 'Canceled', 'Canceled'


    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'Credit Card', 'Credit Card'
        PAYPAL = 'PayPal', 'PayPal'
        CASH_ON_DELIVERY = 'Cash on Delivery', 'Cash on Delivery'
        MOBILE_MONEY = 'Mobile Money', 'Mobile Money'
        BANK_TRANSFER = 'Bank Transfer', 'Bank Transfer'
        


    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING, null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders", db_index=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name="orders", null=True, blank=True, db_index=True)
    
    shipping_address = models.TextField(null=True, blank=True,)

    payment_method = models.CharField(max_length=100, choices=PaymentMethod.choices, default=PaymentMethod.CASH_ON_DELIVERY, null=True, blank=True)

    extra_notes = models.TextField(null=True, blank=True)


    def __str__(self) -> str:
        return f"Order {self.id} by ({self.customer.full_name}) - ({self.status})"

    def get_order_items(self):
        order_items = []

        for order_item in OrderItem.objects.filter(order=self):
            order_items.append(
                {
                    "product": {
                        "name": order_item.product.name,
                        "price": order_item.product.price,
                        "image": order_item.product.image
                    },
                    "quantity": order_item.quantity,
                    "sub_total_price": order_item.sub_total_price
                }
            )

        return order_items

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created"]
        # unique_together = ["customer", "cart"]
        


    def save(self, **kwargs):
        # if order.cart has Order Items update total_price
        if self.cart:
            self.total_price = sum([order_item.sub_total_price for order_item in OrderItem.objects.filter(order=self)])

        if not self.shipping_address:
            if self.customer.address:
                self.shipping_address = self.customer.address

        super().save(**kwargs)
        



class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    sub_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = "order_items"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["-created"]

    
    def save(self, **kwargs):
        self.sub_total_price = self.product.price * self.quantity
        super().save(**kwargs)
    

        


# class OrderRefund(TimeStampedModel):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="refund")
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     reason = models.TextField()
#     status = models.CharField(max_length=50, choices=Order.OrderStatus.choices, default=Order.OrderStatus.PENDING)
#     notes = models.TextField(null=True, blank=True)
#     customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="order_refunds")
#     complaint = models.TextField(null=True, blank=True)

#     class Meta:
#         db_table = "order_refunds"
#         verbose_name = "Order Refund"
#         verbose_name_plural = "Order Refunds"
#         ordering = ["-created"]
        
    


# class OrderiItemReturn(TimeStampedModel):
#     order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name="return")
#     status = models.CharField(max_length=50, choices=Order.OrderStatus.choices, default=Order.OrderStatus.PENDING)
#     notes = models.TextField(null=True, blank=True)
#     customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="order_returns")
#     complaint = models.TextField(null=True, blank=True)
      

#     class Meta:
#         db_table = "order_returns"
#         verbose_name = "Order Return"
#         verbose_name_plural = "Order Returns"
#         ordering = ["-created"]



# class OrderExchange(TimeStampedModel):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="exchange")
#     status = models.CharField(max_length=50, choices=Order.OrderStatus.choices, default=Order.OrderStatus.PENDING)
#     notes = models.TextField(null=True, blank=True)
#     customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="order_exchanges")

        