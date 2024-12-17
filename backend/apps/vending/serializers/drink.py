from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework.exceptions import ValidationError
from apps.vending.models import DrinkType, DrinkVolume, DrinkHistory


class DrinkVolumeSerializer(ModelSerializer):
    class Meta:
        model = DrinkVolume
        fields = ["id", "volume_ml", "price"]


class DrinkTypeSerializer(ModelSerializer):

    class Meta:
        model = DrinkType
        fields = ["id", "name"]


class DrinkBuySerializer(ModelSerializer):
    volume = PrimaryKeyRelatedField(
        source="drink", queryset=DrinkVolume.objects.all(), write_only=True
    )

    class Meta:
        model = DrinkHistory
        fields = ["volume"]

    def validate(self, attrs):
        place = self.context.get("place")
        if not attrs["drink"] in DrinkVolume.objects.filter(drink_type__place=place):
            raise ValidationError(
                "Данная позиция не входит в меню автомата. Выберите другую позицию"
            )
        return attrs

    def create(self, validated_data):
        place = self.context.get("place")
        drink = validated_data.pop("drink")
        validated_data["user"] = self.context.get("request").user
        validated_data["place"] = place
        validated_data["partner"] = place.partner
        validated_data["price"] = drink.price
        validated_data["drink_name"] = drink.name
        return super().create(validated_data)


class DrinkHistorySerializer(ModelSerializer):
    class Meta:
        model = DrinkHistory
        fields = ["drink_name", "place_address", "purchase_date"]
