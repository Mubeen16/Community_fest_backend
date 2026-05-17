from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.waitlist.serializers import WaitlistSerializer
from common.mixins import EventScopedMixin
from common.permissions import IsPublic


class WaitlistCreateView(EventScopedMixin, CreateAPIView):
    serializer_class = WaitlistSerializer
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
                "detail": "You're on the list! We'll notify you when registration opens.",
                "email": serializer.validated_data["email"],
            },
            status=status.HTTP_201_CREATED,
        )
