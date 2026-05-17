from django.db import models


class SponsorLead(models.Model):
    class TierInterest(models.TextChoices):
        TITLE_SPONSOR = "title_sponsor", "Title Sponsor (from £10,000)"
        DIAMOND = "diamond", "Diamond (from £5,000)"
        PLATINUM = "platinum", "Platinum (from £3,000)"
        GOLD = "gold", "Gold (£2,000)"
        SILVER = "silver", "Silver (£1,000)"
        UNDECIDED = "undecided", "Not sure yet"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        IN_DISCUSSION = "in_discussion", "In Discussion"
        CONFIRMED = "confirmed", "Confirmed"
        DECLINED = "declined", "Declined"
        LOST = "lost", "Lost"

    ACTIVE_STATUSES = (
        Status.NEW,
        Status.CONTACTED,
        Status.IN_DISCUSSION,
        Status.CONFIRMED,
    )

    event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        related_name="sponsor_leads",
    )
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    tier_interest = models.CharField(
        max_length=30,
        choices=TierInterest.choices,
        default=TierInterest.UNDECIDED,
    )
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    confirmed_tier = models.CharField(max_length=30, blank=True)
    confirmed_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    invoice_sent = models.BooleanField(default=False)
    payment_received = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.company_name} - {self.event} ({self.status})"
