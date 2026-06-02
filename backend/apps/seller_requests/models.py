from django.conf import settings
from django.db import models


class SellerRequestStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"


class SellerRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller_requests",
    )

    restaurant_name = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=SellerRequestStatus.choices,
        default=SellerRequestStatus.PENDING,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"