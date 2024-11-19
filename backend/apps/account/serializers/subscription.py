from rest_framework.serializers import ModelSerializer, Serializer, IntegerField
from rest_framework.exceptions import ValidationError
from apps.account.models import UserSubscription
from apps.vending.models import Place, SubscriptionTariff


class UserSubscriptionPlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "address"]


class UserSubscriptionSerializer(ModelSerializer):
    place = UserSubscriptionPlaceSerializer()

    class Meta:
        model = UserSubscription
        fields = ["id", "place", "status", "expire_date", "today_cups"]


class BuySubscriptionSerializer(Serializer):
    place_id = IntegerField()
    tariff_id = IntegerField()

    def validate(self, attrs):
        try:
            attrs["place"] = Place.objects.get(id=attrs["place_id"])
            attrs["tariff"] = SubscriptionTariff.objects.get(id=attrs["tariff_id"])
        except [Place.DoesNotExist, SubscriptionTariff.DoesNotExist]:
            raise ValidationError("Автомат или тариф не найден")
        return attrs

    # def create(self, validated_data):
    #     validated_data["user"] = self.context.get("request").user
    #     validated_data["price"] = validated_data["tariff"].price
    #     return super().create(validated_data)
