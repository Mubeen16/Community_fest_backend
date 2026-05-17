import stripe
from django.conf import settings

from apps.tickets.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(order, success_url, cancel_url):
    """Create a Stripe Checkout Session for an order."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {
                        "name": f"London Community Fest — {order.adult_count} Adult(s)",
                        "description": f"Order {order.reference} · {order.adult_count} adult entry",
                    },
                    "unit_amount": int(order.total_amount * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=order.email,
        metadata={
            "order_id": str(order.id),
            "order_reference": order.reference,
            "event_slug": order.event.slug,
        },
    )

    order.stripe_session_id = session.id
    order.save(update_fields=["stripe_session_id"])

    return session


def handle_checkout_completed(session):
    """Process a successful payment from Stripe webhook."""
    from django.utils import timezone

    from apps.tickets.services.email import send_ticket_confirmation
    from apps.tickets.services.qr import generate_qr_code

    order_id = session.metadata.get("order_id")
    if not order_id:
        return None

    try:
        order = Order.objects.select_related("event", "ticket_type").get(id=order_id)
    except Order.DoesNotExist:
        return None

    if order.status == "paid":
        return order

    order.status = "paid"
    order.paid_at = timezone.now()
    order.stripe_payment_intent_id = session.get("payment_intent", "")
    order.save(update_fields=["status", "paid_at", "stripe_payment_intent_id"])

    order.ticket_type.quantity_sold = Order.objects.filter(
        ticket_type=order.ticket_type, status="paid"
    ).count()
    order.ticket_type.save(update_fields=["quantity_sold"])

    qr_image = generate_qr_code(order.qr_token, order.event.slug)
    send_ticket_confirmation(order, qr_image)

    return order


def verify_webhook_signature(payload, sig_header):
    """Verify Stripe webhook signature. Returns the event or raises ValueError."""
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    return stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
