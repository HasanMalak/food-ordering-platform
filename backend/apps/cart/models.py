from django.conf import settings
from django.db import models

from apps.menu.models import MenuItem


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Cart - {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"