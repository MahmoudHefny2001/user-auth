from django.db import models

from django_extensions.db.models import TimeStampedModel

from users.models import User




class Category(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to="images/products", null=True, blank=True,)
    
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="products")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created"]
    



class ProductReport(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reports")
    total_quantity = models.IntegerField()
    total_sold = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f"{self.product} - {self.user}"
    
    class Meta:
        db_table = "product_reports"
        verbose_name = "Product Report"
        verbose_name_plural = "Product Reports"



class ProductReview(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    review = models.TextField()
    
    def __str__(self):
        return f"{self.product} - {self.user}"
    
    class Meta:
        db_table = "product_reviews"
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"



class ProductAttachment(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attachments")
    attachment = models.FileField(upload_to="images/product_attachments")
    
    def __str__(self):
        return f"{self.product} - {self.attachment}"
    
    class Meta:
        db_table = "product_attachments"
        verbose_name = "Product Attachment"
        verbose_name_plural = "Product Attachments"