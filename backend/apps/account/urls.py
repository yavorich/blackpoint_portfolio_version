from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.account.views import (
    UserProfileAPIView,
    UserSubscriptionViewSet,
    # SubscriptionTariffView,
    DocumentAPIView,
    PaymentWebhookView,
)


router = DefaultRouter()
router.register(
    "profile/subscriptions", UserSubscriptionViewSet, basename="user-subscriptions"
)

urlpatterns = [
    path("profile/", UserProfileAPIView.as_view(), name="profile"),
    # path("tariffs/", SubscriptionTariffView.as_view(), name="subscription-tariffs"),
    path("document/<str:type>/", DocumentAPIView.as_view(), name="document"),
    path(
        "payment/webhook/", PaymentWebhookView.as_view(), name="payment-webhook"
    ),
] + router.urls
