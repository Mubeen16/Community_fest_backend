from rest_framework import serializers

from apps.vendors.models import VendorApplication


class VendorApplicationCreateSerializer(serializers.Serializer):
    business_name = serializers.CharField(max_length=200)
    contact_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    stall_type = serializers.ChoiceField(choices=VendorApplication.StallType.choices)
    description = serializers.CharField()
    halal_certified = serializers.BooleanField(default=False)

    def validate_email(self, value: str) -> str:
        event = self.context["event"]
        if VendorApplication.objects.filter(
            event=event,
            email__iexact=value,
            status__in=VendorApplication.ACTIVE_STATUSES,
        ).exists():
            raise serializers.ValidationError(
                "An application with this email already exists for this event."
            )
        return value

    def validate(self, attrs: dict) -> dict:
        if attrs.get("stall_type") == VendorApplication.StallType.FOOD and not attrs.get(
            "halal_certified"
        ):
            raise serializers.ValidationError(
                {
                    "halal_certified": "Food vendors must confirm halal certification."
                }
            )
        return attrs

    def create(self, validated_data: dict) -> VendorApplication:
        return VendorApplication.objects.create(
            event=self.context["event"],
            **validated_data,
        )
