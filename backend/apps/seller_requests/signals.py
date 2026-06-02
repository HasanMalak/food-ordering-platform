from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import UserRole
from .models import SellerRequest, SellerRequestStatus


@receiver(post_save, sender=SellerRequest)
def update_user_role_on_approval(sender, instance, **kwargs):
    if instance.status == SellerRequestStatus.APPROVED:
        user = instance.user

        if user.role != UserRole.SELLER:
            user.role = UserRole.SELLER
            user.save()