from django.urls import path

from apps.waitlist.views import WaitlistCreateView

urlpatterns = [
    path("", WaitlistCreateView.as_view(), name="waitlist-create"),
]
