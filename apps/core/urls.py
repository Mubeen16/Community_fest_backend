from django.urls import path

from apps.core.views import EventDetailView

urlpatterns = [
    path("", EventDetailView.as_view(), name="event-detail"),
]
