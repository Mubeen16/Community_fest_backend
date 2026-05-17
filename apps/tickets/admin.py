from django.contrib import admin

from apps.tickets.models import Order, TicketType


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "event", "created_at")
    list_filter = ("event", "is_active")
    list_editable = ("is_active",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "name",
        "email",
        "adult_count",
        "total_amount",
        "status",
        "checked_in",
        "paid_at",
        "created_at",
    )
    list_filter = ("status", "event", "checked_in")
    search_fields = ("reference", "name", "email", "qr_token")
    readonly_fields = (
        "reference",
        "qr_token",
        "stripe_session_id",
        "stripe_payment_intent_id",
        "created_at",
        "paid_at",
    )

    fieldsets = (
        (
            "Buyer",
            {
                "fields": ("name", "email", "phone"),
            },
        ),
        (
            "Order",
            {
                "fields": ("reference", "ticket_type", "adult_count", "total_amount"),
            },
        ),
        (
            "Payment",
            {
                "fields": (
                    "status",
                    "stripe_session_id",
                    "stripe_payment_intent_id",
                    "paid_at",
                ),
            },
        ),
        (
            "QR Ticket",
            {
                "fields": ("qr_token", "checked_in", "checked_in_at"),
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at",),
            },
        ),
    )
