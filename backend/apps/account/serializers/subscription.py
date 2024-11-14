from rest_framework.serializers import ModelSerializer
from apps.account.models import UserSubscription
from apps.vending.models import Place


class UserSubscriptionPlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "address"]


class UserSubscriptionsSerializer(ModelSerializer):
    place = UserSubscriptionPlaceSerializer()

    class Meta:
        model = UserSubscription
        fields = ["id", "place", "status", "expire_date"]
