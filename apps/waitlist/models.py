from django.db import models


class WaitlistEntry(models.Model):
    event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        related_name="waitlist_entries",
    )
    email = models.EmailField()
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["event", "email"]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.email} - {self.event}"
