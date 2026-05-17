from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.core.models import Event
from apps.core.serializers import EventDetailSerializer


class EventDetailView(RetrieveAPIView):
    serializer_class = EventDetailSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "event_slug"
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Event.objects.filter(status=Event.Status.PUBLISHED)
