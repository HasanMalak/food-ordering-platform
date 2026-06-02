from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import Order

from .models import Payment
from .serializers import (
    PaymentCreateSerializer,
)


class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = (
            PaymentCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        order = Order.objects.get(
            id=serializer.validated_data[
                "order_id"
            ],
            user=request.user,
        )
        if hasattr(order, "payment"):
            return Response(
                {
                    "error": "Payment already exists for this order."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.create(
            order=order,
            payment_method=serializer.validated_data[
                "payment_method"
            ],
            amount=order.total_amount,
        )

        return Response(
            {
                "payment_id": payment.id,
                "transaction_id": (
                    payment.transaction_id
                ),
                "status": payment.status,
            },
            status=status.HTTP_201_CREATED,
        )