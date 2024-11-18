from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.vending.serializers import SubscriptionTariffSerializer
from apps.vending.models import SubscriptionTariff


class SubscriptionTariffView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionTariffSerializer
    queryset = SubscriptionTariff.objects.filter(is_active=True)
