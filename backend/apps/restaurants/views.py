from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantCreateView(
    generics.CreateAPIView
):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if request.user.role != "SELLER":
            return Response(
                {"error": "Only sellers can create restaurants."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if Restaurant.objects.filter(
            seller=request.user
        ).exists():
            return Response(
                {"error": "Restaurant already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            seller=request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class MyRestaurantView(
    generics.RetrieveUpdateAPIView
):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Restaurant.objects.get(
            seller=self.request.user
        )