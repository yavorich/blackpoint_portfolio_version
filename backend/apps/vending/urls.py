from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.vending.views import PlaceViewSet, SubscriptionTariffView

router = DefaultRouter()
router.register("places", PlaceViewSet, basename="places")

urlpatterns = [
    path("tariffs/", SubscriptionTariffView.as_view(), name="tariffs-list")
] + router.urls
