from django.db import models

from django_extensions.db.models import TimeStampedModel

from apps.products.models import Product
from apps.customers.models import Customer

from .validators import validate_rating


class ProductReview(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(validators=[validate_rating])
    review = models.TextField(null=True, blank=True, )
    


    def __str__(self):
        return f"{self.product} - {self.customer.full_name}"
    
    class Meta:
        db_table = "product_reviews"
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"
        ordering = ["-created"]
        unique_together = ["product", "customer"]
    
