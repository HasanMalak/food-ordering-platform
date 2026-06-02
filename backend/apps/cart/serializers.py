from rest_framework import serializers

from apps.menu.models import MenuItem
from .models import Cart, CartItem


class AddToCartSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CartItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = (
            "id",
            "menu_item",
            "quantity",
            "unit_price",
            "subtotal",
        )


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            "id",
            "items",
            "created_at",
            "updated_at",
        )