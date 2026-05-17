from io import BytesIO

import qrcode
from django.conf import settings


def generate_qr_code(token, event_slug):
    """Generate a QR code PNG as bytes. QR encodes the check-in verification URL."""
    base_url = getattr(settings, "API_BASE_URL", "http://localhost:8000")
    verify_url = f"{base_url}/api/v1/events/{event_slug}/checkin/{token}/"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(verify_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#1A2A14", back_color="#FFFFFF")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
