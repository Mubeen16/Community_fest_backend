from rest_framework import serializers

from apps.core.models import Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("name", "slug", "date", "venue_name", "status")


class EventDetailSerializer(serializers.ModelSerializer):
    organisation_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "name",
            "slug",
            "description",
            "date",
            "start_time",
            "end_time",
            "venue_name",
            "venue_address",
            "venue_postcode",
            "status",
            "expected_attendance",
            "organisation_name",
        )

    def get_organisation_name(self, obj: Event) -> str:
        return obj.organisation.name
