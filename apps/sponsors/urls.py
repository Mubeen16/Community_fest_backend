from django.urls import path

from apps.sponsors.views import SponsorLeadCreateView

urlpatterns = [
    path("", SponsorLeadCreateView.as_view(), name="sponsor-enquiry"),
]
