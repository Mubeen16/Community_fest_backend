from rest_framework import serializers

from apps.sponsors.models import SponsorLead


class SponsorLeadCreateSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=200)
    contact_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    tier_interest = serializers.ChoiceField(choices=SponsorLead.TierInterest.choices)
    message = serializers.CharField(required=False, allow_blank=True, default="")

    def validate_email(self, value: str) -> str:
        event = self.context["event"]
        if SponsorLead.objects.filter(
            event=event,
            email__iexact=value,
            status__in=SponsorLead.ACTIVE_STATUSES,
        ).exists():
            raise serializers.ValidationError(
                "An enquiry with this email already exists."
            )
        return value

    def create(self, validated_data: dict) -> SponsorLead:
        return SponsorLead.objects.create(
            event=self.context["event"],
            **validated_data,
        )
