from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.vending.models import Place
from apps.account.models import UserSubscription


class UserSubscriptionStatusSerializer(ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ["status", "expire_date"]


class PlaceSerializer(ModelSerializer):
    subscription = SerializerMethodField()

    class Meta:
        model = Place
        fields = ["id", "address", "subscription"]

    def get_subscription(self, obj: Place):
        user = self.context.get("request").user
        subscription = UserSubscription.objects.filter(user=user, place=obj).first()
        if subscription:
            return UserSubscriptionStatusSerializer(subscription).data
        return None
