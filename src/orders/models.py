from django.db import models

from django_extensions.db.models import TimeStampedModel

from customers.models import Customer

from products.models import Product


class Order(TimeStampedModel):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created"]
        
    def __str__(self):
        return f"Order {self.id}"
    



class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = "order_items"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["-created"]
        
    def __str__(self):
        return f"Order Item {self.id}"