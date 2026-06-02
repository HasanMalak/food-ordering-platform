from django.db.models import Count, Sum
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import Order
from apps.restaurants.models import Restaurant

from .serializers import (
    SellerOrderSerializer,
    OrderStatusUpdateSerializer,
)


class SellerOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "SELLER":
            return Response(
                {"error": "Seller access required."},
                status=status.HTTP_403_FORBIDDEN,
            )

        restaurant = Restaurant.objects.get(
            seller=request.user
        )

        orders = Order.objects.filter(
            restaurant=restaurant
        ).order_by("-created_at")

        serializer = SellerOrderSerializer(
            orders,
            many=True,
        )

        return Response(serializer.data)


class SellerOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        restaurant = Restaurant.objects.get(
            seller=request.user
        )

        order = Order.objects.get(
            id=pk,
            restaurant=restaurant,
        )

        serializer = OrderStatusUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        order.status = serializer.validated_data[
            "status"
        ]

        order.save()

        return Response(
            {"message": "Order status updated"}
        )


class SellerSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        restaurant = Restaurant.objects.get(
            seller=request.user
        )

        orders = Order.objects.filter(
            restaurant=restaurant
        )

        data = {
            "total_orders": orders.count(),
            "pending_orders": orders.filter(
                status="PENDING"
            ).count(),
            "completed_orders": orders.filter(
                status="DELIVERED"
            ).count(),
            "revenue": (
                orders.aggregate(
                    total=Sum("total_amount")
                )["total"]
                or 0
            ),
        }

        return Response(data)