from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import SellerRequest
from .serializers import SellerRequestSerializer


class SellerRequestListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = SellerRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SellerRequest.objects.filter(
            user=self.request.user
        ).order_by("-created_at")