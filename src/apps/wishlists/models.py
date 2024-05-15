from django.db import models

from django_extensions.db.models import TimeStampedModel

from apps.customers.models import Customer
from apps.products.models import Product


class Wishlist(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="wishlists", db_index=True)
    
    class Meta:
        db_table = "wishlists"
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
        ordering = ["-created"]
        

    def __str__(self):
        return f"{self.customer}"



class WishlistItem(TimeStampedModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="wishlist_items", db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")
    
    class Meta:
        db_table = "wishlist_items"
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"
        ordering = ["-created"]
        

    def __str__(self):
        return f"{self.wishlist} - {self.product}"