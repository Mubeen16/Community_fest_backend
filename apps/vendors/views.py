from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.vendors.serializers import VendorApplicationCreateSerializer
from common.mixins import EventScopedMixin
from common.permissions import IsPublic


class VendorApplicationCreateView(EventScopedMixin, CreateAPIView):
    serializer_class = VendorApplicationCreateSerializer
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
                "detail": "Application received! We'll be in touch within 5 working days.",
                "business_name": serializer.validated_data["business_name"],
            },
            status=status.HTTP_201_CREATED,
        )
