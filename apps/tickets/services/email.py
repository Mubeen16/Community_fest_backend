import logging
from email.mime.image import MIMEImage

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


def send_ticket_confirmation(order, qr_image_bytes):
    """Send confirmation email with QR code attached as inline image."""
    subject = f"Your London Community Fest tickets ✓ ({order.reference})"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@communityfest.uk")

    text_content = f"""
Hi {order.name},

Your order is confirmed!

Order: {order.reference}
Adults: {order.adult_count}
Total paid: £{order.total_amount}

Event: {order.event.name}
Date: Sunday, 12 July 2026 · 11am – 7pm
Venue: Kennington Park, London SE11 4AX

Show your QR code at the gate for entry.
Children under 10 enter free with an adult — no ticket needed.

See you there!
London Community Fest Team
""".strip()

    html_content = f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <h2 style="color: #1A2A14;">Your tickets are confirmed! ✓</h2>
    
    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
        <tr><td style="padding: 8px 0; color: #666;">Order</td><td style="padding: 8px 0; font-weight: bold;">{order.reference}</td></tr>
        <tr><td style="padding: 8px 0; color: #666;">Name</td><td style="padding: 8px 0; font-weight: bold;">{order.name}</td></tr>
        <tr><td style="padding: 8px 0; color: #666;">Adults</td><td style="padding: 8px 0; font-weight: bold;">{order.adult_count}</td></tr>
        <tr><td style="padding: 8px 0; color: #666;">Total</td><td style="padding: 8px 0; font-weight: bold;">£{order.total_amount}</td></tr>
    </table>
    
    <div style="background: #F5EFE3; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
        <p style="margin: 0 0 10px; font-weight: bold; color: #1A2A14;">Your QR Code</p>
        <p style="margin: 0 0 15px; color: #666; font-size: 14px;">Show this at the gate</p>
        <img src="cid:qr_code" alt="QR Code for entry" style="width: 200px; height: 200px;" />
    </div>
    
    <div style="background: #1A2A14; color: #F0E6D0; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <p style="margin: 0; font-weight: bold;">📅 Sunday, 12 July 2026 · 11am – 7pm</p>
        <p style="margin: 8px 0 0; ">📍 Kennington Park, London SE11 4AX</p>
    </div>
    
    <p style="color: #666; font-size: 14px;">Children under 10 enter free with an adult — no ticket needed.</p>
    
    <p style="color: #999; font-size: 12px; margin-top: 30px;">London Community Fest · South Indian Community UK</p>
</div>
""".strip()

    try:
        email = EmailMultiAlternatives(subject, text_content, from_email, [order.email])
        email.attach_alternative(html_content, "text/html")

        qr_image = MIMEImage(qr_image_bytes, _subtype="png")
        qr_image.add_header("Content-ID", "<qr_code>")
        qr_image.add_header("Content-Disposition", "inline", filename="ticket-qr.png")
        email.attach(qr_image)

        email.send(fail_silently=False)
        logger.info("Ticket confirmation sent to %s for %s", order.email, order.reference)
    except Exception as e:
        logger.error("Failed to send ticket email for %s: %s", order.reference, e)
