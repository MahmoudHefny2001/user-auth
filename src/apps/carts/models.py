from django.db import models

from django_extensions.db.models import TimeStampedModel

from apps.customers.models import Customer

from apps.products.models import Product


class Cart(TimeStampedModel):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="carts", db_index=True,)

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-created"]
        # 
        

    def __str__(self):
        return f"Cart {self.id} for {self.customer.full_name}"



class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items", db_index=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE,)

    item_quantity = models.PositiveIntegerField(default=1, blank=True, null=True)

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ["-created"]
        unique_together = ["cart", "product"]
        

    def __str__(self):
        return f"Cart Item {self.id}"
    
    
    def get_sub_total(self):
        return self.product.price * self.item_quantity
    
    def save(self, **kwargs):
        if not self.item_quantity:
            self.item_quantity = 1
        super(CartItem, self).save(**kwargs)
