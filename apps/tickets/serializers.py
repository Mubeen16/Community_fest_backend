from rest_framework import serializers

from apps.tickets.models import Order, TicketType


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ("id", "name", "price", "description", "is_active")
        read_only_fields = fields


class CheckoutSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    adult_count = serializers.IntegerField(min_value=1, max_value=10)
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()

    def validate_adult_count(self, value: int) -> int:
        if value < 1:
            raise serializers.ValidationError("At least 1 adult required.")
        return value


class OrderConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "reference",
            "name",
            "email",
            "adult_count",
            "total_amount",
            "status",
            "qr_token",
            "checked_in",
            "paid_at",
        )
        read_only_fields = fields
