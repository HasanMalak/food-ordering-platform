from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.restaurants.models import Restaurant

from .models import MenuItem
from .serializers import MenuItemSerializer


class MenuItemListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant = Restaurant.objects.get(
            seller=self.request.user
        )

        return MenuItem.objects.filter(
            restaurant=restaurant
        )

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(
            seller=self.request.user
        )

        serializer.save(
            restaurant=restaurant
        )


class MenuItemDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant = Restaurant.objects.get(
            seller=self.request.user
        )

        return MenuItem.objects.filter(
            restaurant=restaurant
        )