from rest_framework.serializers import ModelSerializer
from apps.support.models import SupportRequest


class SupportRequestSerializer(ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = ["message"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)
