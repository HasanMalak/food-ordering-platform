from rest_framework import serializers

from apps.categories.models import Category
from .models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = "__all__"
        read_only_fields = (
            "id",
            "restaurant",
            "created_at",
            "updated_at",
        )

    def validate_category(self, category):
        request = self.context["request"]

        restaurant = request.user.restaurant

        if category.restaurant != restaurant:
            raise serializers.ValidationError(
                "Invalid category."
            )

        return category