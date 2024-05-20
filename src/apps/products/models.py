from django.db import models

from django_extensions.db.models import TimeStampedModel

from decimal import Decimal

from apps.merchants.models import Merchant

import uuid

class Category(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(TimeStampedModel):

    bar_code = models.CharField(max_length=255, null=True, blank=True, unique=True, db_index=True,)

    name = models.CharField(max_length=255)
    
    description = models.TextField()
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    quantity = models.IntegerField()

    image = models.ImageField(upload_to="images/products/", null=True, blank=True, max_length=500)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)

    available = models.BooleanField(default=True, null=True, blank=True)
    
    on_sale = models.BooleanField(null=True, blank=True)
    
    sale_percent = models.IntegerField(null=True, blank=True)
    
    price_after_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    average_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True,)
    
    merchant = models.ForeignKey(Merchant, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)

    tag = models.CharField(max_length=255, null=True, blank=True)


    def get_reviews(self):
        from apps.reviews.models import ProductReview
        # return json serializable reviews
        reviews = []
        for review in ProductReview.objects.filter(product=self):
            reviews.append(
                {
                    "rating": review.rating,
                    "review": review.review,
                    "customer": {
                        "full_name": review.customer.full_name,
                        # "image": review.customer.get_image_url()
                    }
                }
            )
        return reviews

    
    def get_attachments(self):
        from .serializers import ProductAttachmentSerializer
        return ProductAttachmentSerializer(ProductAttachment.objects.filter(product=self), many=True).data
    
    

    def get_colors(self):
        from .serializers import ProductColorSerializer
        return ProductColorSerializer(ProductColor.objects.filter(product=self), many=True).data


    def save(self, **kwargs):
        if self.on_sale:
            self.price_after_sale = self.price - (self.price * Decimal(self.sale_percent) / 100)

        if not self.bar_code:
            self.bar_code = uuid.uuid4().hex[:15].upper()

        super(Product, self).save(**kwargs)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created"]



class ProductAttachment(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attachments")
    attachment = models.FileField(upload_to="images/product_attachments")

    def get_attachment_url(self):
        # return the full http url of the attachment
        if self.attachment:
            # if settings.HOST_URL:
                # return f"{settings.HOST_URL}{self.attachment.url}"
            return self.attachment.url
        return None
    
    def __str__(self):
        return f"{self.product} - {self.attachment}"
    
    class Meta:
        db_table = "product_attachments"
        verbose_name = "Product Attachment"
        verbose_name_plural = "Product Attachments"
        



class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors", null=False, blank=False,) # bigint
    color = models.CharField(max_length=255, null=False, blank=False,)
    
    def __str__(self):
        return f"{self.product} - {self.color}"
    
    class Meta:
        db_table = "product_colors"
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"
        unique_together = ('product', 'color')
    