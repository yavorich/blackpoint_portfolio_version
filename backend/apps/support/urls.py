from django.urls import path

from apps.support.views import SupportRequestView


urlpatterns = [
    path("support/", SupportRequestView.as_view(), name="support"),
]
