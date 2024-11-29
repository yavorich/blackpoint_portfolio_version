from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    IntegerField,
    EmailField,
    BooleanField,
)
from rest_framework.exceptions import ValidationError
from apps.account.models import UserSubscription
from apps.vending.models import Place, SubscriptionTariff
from phonenumber_field.serializerfields import PhoneNumberField


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
    phone = PhoneNumberField(required=False)
    email = EmailField(required=False)
    opt_in_consent = BooleanField()

    def validate(self, attrs):
        try:
            attrs["place"] = Place.objects.get(id=attrs.pop("place_id"))
            attrs["tariff"] = SubscriptionTariff.objects.get(id=attrs.pop("tariff_id"))
        except Place.DoesNotExist:
            raise ValidationError({"place_id": "Автомат не найден"})
        except SubscriptionTariff.DoesNotExist:
            raise ValidationError({"tariff_id": "Тариф не найден"})

        user = self.context.get("request").user

        # Проверка phone
        phone = attrs.get("phone")
        if phone:
            user.phone = phone  # Обновляем номер телефона пользователя
            user.save(update_fields=["phone"])
        else:
            phone = user.phone
            if not phone:
                raise ValidationError({"phone": "Необходимо указать номер телефона"})
        attrs["phone"] = phone

        # Проверка email
        email = attrs.get("email")
        if email:
            user.email = email  # Обновляем email пользователя
            user.save(update_fields=["email"])
        else:
            email = user.email
            if not email:
                raise ValidationError(
                    {"email": "Необходимо указать адрес электронной почты"}
                )
        attrs["email"] = email

        attrs["partner"] = attrs["place"].partner

        return attrs
