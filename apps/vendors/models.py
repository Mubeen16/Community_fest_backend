from django.db import models


class VendorApplication(models.Model):
    class StallType(models.TextChoices):
        FOOD = "food", "Food"
        FASHION = "fashion", "Fashion"
        BUSINESS = "business", "Business"
        ARTS = "arts", "Arts"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONTACTED = "contacted", "Contacted"
        DOCUMENTS_REQUESTED = "documents_requested", "Documents Requested"
        DOCUMENTS_COMPLETE = "documents_complete", "Documents Complete"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    ACTIVE_STATUSES = (
        Status.PENDING,
        Status.CONTACTED,
        Status.DOCUMENTS_REQUESTED,
        Status.DOCUMENTS_COMPLETE,
        Status.APPROVED,
    )

    event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        related_name="vendor_applications",
    )

    business_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    stall_type = models.CharField(
        max_length=20,
        choices=StallType.choices,
        default=StallType.OTHER,
    )
    description = models.TextField()

    doc_lambeth_questionnaire = models.BooleanField(
        default=False,
        verbose_name="Lambeth Food H&S Questionnaire",
    )
    doc_public_liability = models.BooleanField(
        default=False,
        verbose_name="Public Liability Insurance",
    )
    doc_hygiene_certificate = models.BooleanField(
        default=False,
        verbose_name="Food Hygiene Training Certificate",
    )
    doc_menu = models.BooleanField(
        default=False,
        verbose_name="Menu / Description",
    )
    doc_gas_safety = models.BooleanField(
        default=False,
        verbose_name="Gas Safety Certificate",
    )
    doc_allergen_matrix = models.BooleanField(
        default=False,
        verbose_name="Allergen Matrix",
    )

    halal_certified = models.BooleanField(
        default=False,
        verbose_name="Halal Certified",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    admin_notes = models.TextField(blank=True)
    stall_location = models.CharField(max_length=100, blank=True)
    fee_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    fee_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.business_name} - {self.event} ({self.status})"

    @property
    def documents_complete_count(self) -> int:
        doc_fields = (
            self.doc_lambeth_questionnaire,
            self.doc_public_liability,
            self.doc_hygiene_certificate,
            self.doc_menu,
            self.doc_gas_safety,
            self.doc_allergen_matrix,
        )
        return sum(1 for field in doc_fields if field)

    @property
    def documents_total(self) -> int:
        return 6

    @property
    def is_food_vendor(self) -> bool:
        return self.stall_type == self.StallType.FOOD
