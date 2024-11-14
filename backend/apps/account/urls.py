from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.account.views import UserProfileAPIView, UserSubscriptionViewSet


router = DefaultRouter()
router.register("subscriptions", UserSubscriptionViewSet, basename="user-subscriptions")

urlpatterns = [
    path("profile/", UserProfileAPIView.as_view(), name="profile"),
] + router.urls
