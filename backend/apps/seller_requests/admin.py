from django.contrib import admin
from .models import SellerRequest


@admin.register(SellerRequest)
class SellerRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "restaurant_name",
        "status",
        "created_at",
    )

    list_filter = ("status",)

    search_fields = (
        "restaurant_name",
        "business_name",
        "user__username",
    )