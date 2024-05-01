from django.db import models

from django_extensions.db.models import TimeStampedModel

from apps.customers.models import Customer
from apps.products.models import Product


class Wishlist(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(Product, related_name="wishlists", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "wishlists"
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
        ordering = ["-created"]
        unique_together = ["customer", "product"]

    def __str__(self):
        return f"{self.customer} - {self.product}"
