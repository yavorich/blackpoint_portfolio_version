from rest_framework.serializers import ModelSerializer

from apps.account.models import User


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "avatar",
            "email",
            "phone",
            "has_active_subscriptions",
            "subscribed_until",
        ]
