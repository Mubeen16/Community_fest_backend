from django.contrib import admin

from apps.vendors.models import VendorApplication


@admin.register(VendorApplication)
class VendorApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "contact_name",
        "stall_type",
        "status",
        "doc_progress",
        "fee_display",
        "fee_paid",
        "created_at",
    )
    list_filter = ("status", "stall_type", "event", "fee_paid", "halal_certified")
    search_fields = ("business_name", "contact_name", "email")
    list_editable = ("status", "fee_paid")
    readonly_fields = ("created_at", "updated_at", "doc_progress")

    fieldsets = (
        (
            "Application Details",
            {
                "fields": (
                    "business_name",
                    "contact_name",
                    "email",
                    "phone",
                    "stall_type",
                    "description",
                ),
            },
        ),
        (
            "Halal Compliance",
            {
                "fields": ("halal_certified",),
                "description": "Required for all food vendors",
            },
        ),
        (
            "Lambeth Council Documents (Food Vendors Only)",
            {
                "fields": (
                    "doc_lambeth_questionnaire",
                    "doc_public_liability",
                    "doc_hygiene_certificate",
                    "doc_menu",
                    "doc_gas_safety",
                    "doc_allergen_matrix",
                ),
                "description": (
                    "Track documents collected in person, via WhatsApp, or email. "
                    "All 6 required for food vendors before council approval."
                ),
            },
        ),
        (
            "Stall Allocation",
            {
                "fields": ("stall_location", "fee_amount", "fee_paid"),
            },
        ),
        (
            "Review",
            {
                "fields": ("status", "admin_notes"),
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    @admin.display(description="Documents")
    def doc_progress(self, obj: VendorApplication) -> str:
        if obj.is_food_vendor:
            return f"{obj.documents_complete_count}/{obj.documents_total} docs"
        return "N/A"

    @admin.display(description="Fee")
    def fee_display(self, obj: VendorApplication) -> str:
        if obj.fee_amount is not None:
            return f"£{obj.fee_amount:,.2f}"
        return "—"
