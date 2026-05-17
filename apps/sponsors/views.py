from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.sponsors.serializers import SponsorLeadCreateSerializer
from common.mixins import EventScopedMixin
from common.permissions import IsPublic


class SponsorLeadCreateView(EventScopedMixin, CreateAPIView):
    serializer_class = SponsorLeadCreateSerializer
    permission_classes = [IsPublic]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["event"] = self.get_event()
        return context

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "detail": "Thank you for your interest! Our team will be in touch within 48 hours.",
                "company_name": serializer.validated_data["company_name"],
            },
            status=status.HTTP_201_CREATED,
        )
