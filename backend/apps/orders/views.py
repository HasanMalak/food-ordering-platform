from decimal import Decimal

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        cart = Cart.objects.get(
            user=request.user
        )

        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response(
                {
                    "error": "Cart is empty."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        restaurant = (
            cart_items.first()
            .menu_item
            .restaurant
        )

        order = Order.objects.create(
            user=request.user,
            restaurant=restaurant,
        )

        total_amount = Decimal("0.00")

        for item in cart_items:

            subtotal = (
                item.quantity
                * item.unit_price
            )

            OrderItem.objects.create(
                order=order,
                menu_item_name=item.menu_item.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=subtotal,
            )

            total_amount += subtotal

        order.total_amount = total_amount
        order.save()

        cart_items.delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderListView(
    generics.ListAPIView
):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


class OrderDetailView(
    generics.RetrieveAPIView
):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        )