from django.db import models

from django_extensions.db.models import TimeStampedModel


class Whishlist(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="whishlists")
    products = models.ManyToManyField("products.Product", related_name="whishlists")
    
    class Meta:
        db_table = "whishlists"
        verbose_name = "Whishlist"
        verbose_name_plural = "Whishlists"
        ordering = ["-created"]
    

    def __str__(self):
        return f"Whishlist {self.id}"
