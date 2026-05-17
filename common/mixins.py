from django.shortcuts import get_object_or_404

from apps.core.models import Event


class EventScopedMixin:
    """
    Base mixin for all views that operate within an event context.
    Extracts event from URL slug, filters querysets, and auto-assigns event on create.
    URL pattern: /api/v1/events/{event_slug}/...
    """

    def get_event(self):
        """Get and cache the event from URL slug."""
        if not hasattr(self, "_event"):
            self._event = get_object_or_404(
                Event,
                slug=self.kwargs["event_slug"],
                status="published",
            )
        return self._event

    def get_queryset(self):
        """Filter queryset to current event only."""
        return super().get_queryset().filter(event=self.get_event())

    def perform_create(self, serializer):
        """Auto-assign event when creating objects."""
        serializer.save(event=self.get_event())
