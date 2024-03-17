from django.db import models

from django_extensions.db.models import TimeStampedModel

from customers.models import Customer

from products.models import Product

from django.core.validators import MinValueValidator, MaxValueValidator


class Order(TimeStampedModel):
    
    class OrderStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        PROCESSING = 'Processing', 'Processing'
        SHIPPED = 'Shipped', 'Shipped'
        DELIVERED = 'Delivered', 'Delivered'
        CANCELED = 'Canceled', 'Canceled'


    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'Credit Card', 'Credit Card'
        DEBIT_CARD = 'Debit Card', 'Debit Card'
        PAYPAL = 'PayPal', 'PayPal'
        CASH_ON_DELIVERY = 'Cash on Delivery', 'Cash on Delivery'
        MOBILE_MONEY = 'Mobile Money', 'Mobile Money'
        BANK_TRANSFER = 'Bank Transfer', 'Bank Transfer'
        OTHER = 'Other', 'Other'


    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    cart = models.ForeignKey('carts.Cart', on_delete=models.DO_NOTHING, related_name="orders", null=True, blank=True)
    
    shipping_address = models.TextField(null=True, blank=True)

    payment_method = models.CharField(max_length=100, choices=PaymentMethod.choices, default=PaymentMethod.CASH_ON_DELIVERY)


    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created"]
        



class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="order_items")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    sub_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = "order_items"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["-created"]
        