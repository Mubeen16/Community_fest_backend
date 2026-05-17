from rest_framework.permissions import BasePermission

from apps.core.models import GateToken, OrganisationMembership


class IsPublic(BasePermission):
    """Allow any request — explicit marker for public endpoints."""

    def has_permission(self, request, view):
        return True


class IsGateVolunteer(BasePermission):
    """Authenticate via gate token in Authorization header."""

    def has_permission(self, request, view):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return False
        return GateToken.objects.filter(
            token=token,
            event__slug=view.kwargs.get("event_slug"),
            is_active=True,
        ).exists()


class IsOrganisationMember(BasePermission):
    """Check authenticated user belongs to the event's organisation."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        event = view.get_event()
        return OrganisationMembership.objects.filter(
            user=request.user,
            organisation=event.organisation,
        ).exists()
