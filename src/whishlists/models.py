from django.db import models

from django_extensions.db.models import TimeStampedModel


class Whishlist(TimeStampedModel):
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, related_name="whishlists")
    product = models.ForeignKey("products.Product", related_name="whishlists", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "whishlists"
        verbose_name = "Whishlist"
        verbose_name_plural = "Whishlists"
        ordering = ["-created"]
    

    def __str__(self):
        return f"{self.customer} - {self.product}"

