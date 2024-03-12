from django.db import models

from django_extensions.db.models import TimeStampedModel

from products.models import Product
from customers.models import Customer

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
    

    # average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, null=True, blank=True, editable=False)
    
    
    # def save(self, **kwargs):
        # super(ProductReview, self).save(**kwargs)
        # self.update_average_rating()
