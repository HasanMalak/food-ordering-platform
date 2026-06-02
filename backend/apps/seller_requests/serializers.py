from rest_framework import serializers

from .models import SellerRequest, SellerRequestStatus


class SellerRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerRequest
        fields = [
            "id",
            "restaurant_name",
            "business_name",
            "phone",
            "address",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "status",
            "created_at",
        ]

    def validate(self, attrs):
        user = self.context["request"].user

        if user.role == "SELLER":
            raise serializers.ValidationError(
                "You are already a seller."
            )

        pending_request_exists = SellerRequest.objects.filter(
            user=user,
            status=SellerRequestStatus.PENDING,
        ).exists()

        if pending_request_exists:
            raise serializers.ValidationError(
                "You already have a pending seller request."
            )

        return attrs

    def create(self, validated_data):
        return SellerRequest.objects.create(
            user=self.context["request"].user,
            **validated_data
        )