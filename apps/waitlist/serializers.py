from rest_framework import serializers

from apps.waitlist.models import WaitlistEntry


class WaitlistSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        email = value.lower()
        event = self.context["event"]
        if WaitlistEntry.objects.filter(event=event, email=email).exists():
            raise serializers.ValidationError(
                "This email is already on the waitlist."
            )
        return email

    def create(self, validated_data: dict) -> WaitlistEntry:
        return WaitlistEntry.objects.create(
            event=self.context["event"],
            email=validated_data["email"],
        )
