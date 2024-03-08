from django.db import models

from django_extensions.db.models import TimeStampedModel



class Cart(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="carts")
    products = models.ManyToManyField("products.Product", related_name="carts")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_ordered = models.BooleanField(default=False)
    
    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-created"]


    def __str__(self):
        return f"Cart {self.id}"
    

    def get_cart_items(self):
        return CartItem.objects.filter(cart=self)



class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.product} - {self.quantity}"
    
    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ["-created"]