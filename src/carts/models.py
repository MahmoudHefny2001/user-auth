from django.db import models

from django_extensions.db.models import TimeStampedModel

from customers.models import Customer

from products.models import Product


class Cart(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="carts")    

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-created"]
        unique_together = ['customer', 'product']

    def __str__(self):
        return f"Cart {self.id}"
    
