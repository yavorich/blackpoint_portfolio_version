from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.vending.views import PlaceViewSet

router = DefaultRouter()
router.register("places", PlaceViewSet, basename="places")

urlpatterns = [] + router.urls
