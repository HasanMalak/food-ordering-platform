from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.restaurants.models import Restaurant

from .models import Category
from .serializers import CategorySerializer


class CategoryListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant = Restaurant.objects.get(
            seller=self.request.user
        )

        return Category.objects.filter(
            restaurant=restaurant
        )

    def create(self, request, *args, **kwargs):

        if request.user.role != "SELLER":
            return Response(
                {
                    "error": "Only sellers can create categories."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        restaurant = Restaurant.objects.get(
            seller=request.user
        )

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            restaurant=restaurant
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )