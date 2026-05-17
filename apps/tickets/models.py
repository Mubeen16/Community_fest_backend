import secrets

from django.db import models
from django.utils import timezone


class TicketType(models.Model):
    event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        related_name="ticket_types",
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    quantity_sold = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} - £{self.price}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"
        EXPIRED = "expired", "Expired"

    STATUS_CHOICES = Status.choices

    event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    reference = models.CharField(max_length=30, unique=True, db_index=True)

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    adult_count = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)

    stripe_session_id = models.CharField(max_length=200, blank=True, db_index=True)
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=Status.PENDING,
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    qr_token = models.CharField(max_length=30, unique=True, db_index=True)

    checked_in = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.reference} - {self.name} ({self.adult_count} adults)"

    def save(self, *args, **kwargs) -> None:
        if not self.reference:
            self.reference = self._generate_reference()
        if not self.qr_token:
            self.qr_token = f"LCF-{secrets.token_hex(8)}"
        super().save(*args, **kwargs)

    def _generate_reference(self) -> str:
        date_str = timezone.now().strftime("%Y%m%d")
        return f"LCF-{date_str}-{secrets.token_hex(3).upper()}"

    @property
    def total_people(self) -> int:
        return self.adult_count

    @property
    def display_summary(self) -> str:
        label = "adult" if self.adult_count == 1 else "adults"
        return f"{self.name} — {self.adult_count} {label}"
