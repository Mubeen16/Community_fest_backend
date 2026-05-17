from django.contrib import admin

from apps.waitlist.models import WaitlistEntry


@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ("email", "event", "confirmed", "created_at")
    list_filter = ("event", "confirmed")
    search_fields = ("email",)
    readonly_fields = ("created_at",)
