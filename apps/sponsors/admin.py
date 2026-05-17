from django.contrib import admin

from apps.sponsors.models import SponsorLead


@admin.register(SponsorLead)
class SponsorLeadAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "contact_name",
        "tier_interest",
        "status",
        "confirmed_amount_display",
        "payment_received",
        "created_at",
    )
    list_filter = (
        "status",
        "tier_interest",
        "event",
        "payment_received",
        "invoice_sent",
    )
    search_fields = ("company_name", "contact_name", "email")
    list_editable = ("status", "payment_received")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Enquiry Details",
            {
                "fields": (
                    "company_name",
                    "contact_name",
                    "email",
                    "phone",
                    "tier_interest",
                    "message",
                ),
            },
        ),
        (
            "Deal Status",
            {
                "fields": (
                    "status",
                    "confirmed_tier",
                    "confirmed_amount",
                    "invoice_sent",
                    "payment_received",
                ),
            },
        ),
        (
            "Internal",
            {
                "fields": ("admin_notes",),
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    @admin.display(description="Amount")
    def confirmed_amount_display(self, obj: SponsorLead) -> str:
        if obj.confirmed_amount is not None:
            return f"£{obj.confirmed_amount:,.2f}"
        return "—"
