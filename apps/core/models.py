import secrets

from django.conf import settings
from django.db import models


class Organisation(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="events",
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue_name = models.CharField(max_length=200)
    venue_address = models.CharField(max_length=300)
    venue_postcode = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    expected_attendance = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return self.name


class OrganisationMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"
        VOLUNTEER = "volunteer", "Volunteer"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "organisation"]

    def __str__(self) -> str:
        return f"{self.user} - {self.organisation} ({self.role})"


class GateToken(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="gate_tokens",
    )
    token = models.CharField(max_length=64, unique=True, db_index=True)
    gate_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.gate_name} - {self.event}"

    def save(self, *args, **kwargs) -> None:
        if not self.token:
            self.token = secrets.token_hex(32)
        super().save(*args, **kwargs)
