import uuid

from django.db import models

from apps.orders.models import Order


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"


class PaymentMethod(models.TextChoices):
    UPI = "UPI", "UPI"
    CARD = "CARD", "Card"
    COD = "COD", "Cash On Delivery"


class Payment(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.SUCCESS,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = (
                str(uuid.uuid4())
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_id