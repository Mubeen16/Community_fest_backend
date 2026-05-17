from django.contrib import admin

from apps.core.models import Event, GateToken, Organisation, OrganisationMembership


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "email", "created_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation", "date", "status", "created_at")
    list_filter = ("status", "organisation")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(OrganisationMembership)
class OrganisationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "organisation", "role", "created_at")
    list_filter = ("role", "organisation")


@admin.register(GateToken)
class GateTokenAdmin(admin.ModelAdmin):
    list_display = ("gate_name", "event", "is_active", "truncated_token", "created_at")
    list_filter = ("event", "is_active")
    readonly_fields = ("token",)

    @admin.display(description="Token")
    def truncated_token(self, obj: GateToken) -> str:
        return f"{obj.token[:8]}…"
