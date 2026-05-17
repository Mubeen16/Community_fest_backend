import csv

from django.contrib import admin
from django.http import HttpResponse

from apps.waitlist.models import WaitlistEntry


@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ("email", "event", "confirmed", "created_at")
    list_filter = ("event", "confirmed")
    search_fields = ("email",)
    readonly_fields = ("created_at",)
    actions = ["export_emails_csv"]

    @admin.action(description="Export emails CSV")
    def export_emails_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="waitlist-export.csv"'

        writer = csv.writer(response)
        writer.writerow(["email", "event", "confirmed", "created_at"])
        for entry in queryset.select_related("event"):
            writer.writerow(
                [
                    entry.email,
                    entry.event.name,
                    entry.confirmed,
                    entry.created_at.isoformat(),
                ]
            )

        return response
