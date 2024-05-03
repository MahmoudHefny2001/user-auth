from django.db import models

from django_extensions.db.models import TimeStampedModel

from django.conf import settings

from decimal import Decimal

from django.contrib.postgres.fields import ArrayField

from django.core.validators import MinValueValidator, MaxValueValidator

from apps.merchants.models import Merchant


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

    bar_code = models.CharField(max_length=255, null=True, blank=True, unique=True, db_index=True)

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to="images/products/", null=True, blank=True, default=None, max_length=400)
    
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="products", null=True, blank=True, default=None)

    available = models.BooleanField(default=True, null=True, blank=True)
    on_sale = models.BooleanField(default=False, null=True, blank=True)
    sale_percent = models.IntegerField(default=0, null=True, blank=True)
    price_after_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    

    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, related_name="products", null=True, blank=True, default=None)


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
        else:
            self.on_sale = False
            self.price_after_sale = self.price
            self.sale_percent = 0
            
        super(Product, self).save(**kwargs)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created"]
        
    
    def get_image_url(self):
        # return the full http url of the image
        if self.image:
            # return f"{settings.HOST_URL}{self.image.url}"
            return self.image.url
        return None



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
    # id bigint
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors", null=False, blank=False,) # bigint
    color = models.CharField(max_length=255, null=False, blank=False,)
    
    def __str__(self):
        return f"{self.product} - {self.color}"
    
    class Meta:
        db_table = "product_colors"
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"
        unique_together = ('product', 'color')