from django.db import models

from django_extensions.db.models import TimeStampedModel

from apps.customers.models import Customer

from apps.products.models import Product


class Cart(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="carts", db_index=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts")    

    item_quantity = models.PositiveIntegerField(default=1, blank=True, null=True)

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-created"]
        # 
        

    def __str__(self):
        return f"Cart {self.id}"
    
    
    def total(self):
        return self.product.price * self.item_quantity
    
    def save(self, **kwargs):
        if not self.item_quantity:
            self.item_quantity = 1
        super(Cart, self).save(**kwargs)
    


    