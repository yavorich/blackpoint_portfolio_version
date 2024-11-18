from rest_framework.serializers import ModelSerializer
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
    class Meta:
        model = DrinkHistory
        fields = ["drink"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        validated_data["place"] = self.context.get("place")
        return super().create(validated_data)


class DrinkHistorySerializer(ModelSerializer):
    class Meta:
        model = DrinkHistory
        fields = ["drink_name", "place_address", "purchase_date"]
