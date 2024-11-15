from rest_framework.serializers import ModelSerializer

from apps.vending.models import SubscriptionTariff


class SubscriptionTariffSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionTariff
        fields = ["id", "name", "days", "cups", "price"]
