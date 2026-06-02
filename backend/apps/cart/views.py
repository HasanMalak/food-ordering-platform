from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.menu.models import MenuItem

from .models import Cart, CartItem
from .serializers import (
    AddToCartSerializer,
    CartSerializer,
)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        menu_item = MenuItem.objects.get(
            id=serializer.validated_data["menu_item_id"]
        )

        quantity = serializer.validated_data[
            "quantity"
        ]

        cart, _ = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = (
            CartItem.objects.get_or_create(
                cart=cart,
                menu_item=menu_item,
                defaults={
                    "quantity": quantity,
                    "unit_price": menu_item.price,
                },
            )
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(
            {"message": "Item added to cart"},
            status=status.HTTP_200_OK,
        )


class CartDetailView(
    generics.RetrieveAPIView
):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(
            user=self.request.user
        )

        return cart