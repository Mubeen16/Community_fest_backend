from django.urls import path

from apps.vendors.views import VendorApplicationCreateView

urlpatterns = [
    path("", VendorApplicationCreateView.as_view(), name="vendor-apply"),
]
