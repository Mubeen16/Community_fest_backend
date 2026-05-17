import logging
from decimal import Decimal

import stripe
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tickets.models import Order, TicketType
from apps.tickets.serializers import (
    CheckoutSerializer,
    OrderConfirmationSerializer,
    TicketTypeSerializer,
)
from apps.tickets.services.stripe import (
    create_checkout_session,
    handle_checkout_completed,
    verify_webhook_signature,
)
from common.mixins import EventScopedMixin
from common.permissions import IsPublic

logger = logging.getLogger(__name__)


class TicketTypeListView(EventScopedMixin, ListAPIView):
    serializer_class = TicketTypeSerializer
    permission_classes = [IsPublic]

    def get_queryset(self):
        return TicketType.objects.filter(event=self.get_event(), is_active=True)


class CheckoutView(EventScopedMixin, CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsPublic]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = self.get_event()
        ticket_type = TicketType.objects.filter(event=event, is_active=True).first()
        if not ticket_type:
            return Response(
                {"detail": "No tickets available for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        adult_count = serializer.validated_data["adult_count"]
        total_amount = Decimal(adult_count) * ticket_type.price

        order = Order.objects.create(
            event=event,
            ticket_type=ticket_type,
            name=serializer.validated_data["name"],
            email=serializer.validated_data["email"],
            phone=serializer.validated_data.get("phone", ""),
            adult_count=adult_count,
            total_amount=total_amount,
            status=Order.Status.PENDING,
        )

        try:
            session = create_checkout_session(
                order,
                serializer.validated_data["success_url"],
                serializer.validated_data["cancel_url"],
            )
        except stripe.StripeError as exc:
            order.status = Order.Status.FAILED
            order.save(update_fields=["status"])
            logger.error("Stripe checkout failed for %s: %s", order.reference, exc)
            return Response(
                {"detail": "Payment service unavailable. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {
                "checkout_url": session.url,
                "order_reference": order.reference,
            },
            status=status.HTTP_201_CREATED,
        )


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    permission_classes = [IsPublic]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = verify_webhook_signature(payload, sig_header)
        except ValueError as exc:
            logger.warning("Stripe webhook signature verification failed: %s", exc)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            if event["type"] == "checkout.session.completed":
                handle_checkout_completed(event["data"]["object"])
        except Exception as exc:
            logger.exception("Stripe webhook processing error: %s", exc)

        return Response(status=status.HTTP_200_OK)


class OrderStatusView(EventScopedMixin, RetrieveAPIView):
    serializer_class = OrderConfirmationSerializer
    permission_classes = [IsPublic]
    lookup_field = "reference"
    lookup_url_kwarg = "reference"

    def get_queryset(self):
        return Order.objects.filter(event=self.get_event())
