from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from apps.account.models import (
    UserSubscription,
    SubscriptionPayment,
)
from apps.vending.models import Place


class UserSubscriptionPlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "address"]


class UserSubscriptionSerializer(ModelSerializer):
    place = UserSubscriptionPlaceSerializer()

    class Meta:
        model = UserSubscription
        fields = ["id", "place", "status", "expire_date", "today_cups"]


class SubscriptionPaymentSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionPayment
        fields = ["place", "tariff"]

    def validate(self, attrs):
        if attrs["tariff"] not in attrs["place"].tariffs.all():
            raise ValidationError("Выбранный тариф недоступен для выбранной точки")

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)
