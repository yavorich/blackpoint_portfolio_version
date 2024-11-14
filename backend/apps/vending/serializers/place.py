from rest_framework.serializers import ModelSerializer

from apps.vending.models import Place
from apps.account.models import UserSubscription


class UserSubscriptionStatusSerializer(ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ["status", "expire_date"]


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "address"]
