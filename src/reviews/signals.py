from .models import ProductReview
from products.models import Product

from django.db.models.signals import post_save, pre_save

from django.dispatch import receiver


@receiver(post_save, sender=ProductReview)
def update_product_rating(sender, instance, created, **kwargs):

    """
    This signal updates the average rating of a product when a new review is created
    it calculates the average rating of the product and updates the product's average_rating field
    by summing up all the ratings of the product's reviews and dividing by the total number of reviews.
    """
    
    product = instance.product
    reviews = ProductReview.objects.filter(product=product)
    total_rating = 0
    for review in reviews:
        total_rating += review.rating
    product.average_rating = total_rating / reviews.count()
    product.save()



