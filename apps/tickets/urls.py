from django.urls import path

from apps.tickets.views import (
    CheckoutView,
    OrderStatusView,
    StripeWebhookView,
    TicketTypeListView,
)

urlpatterns = [
    path("", TicketTypeListView.as_view(), name="ticket-types"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("order/<str:reference>/", OrderStatusView.as_view(), name="order-status"),
]
