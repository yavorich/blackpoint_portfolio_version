from rest_framework.serializers import Serializer, CharField, DateTimeField, UUIDField


class PaymentWebhookSerializer(Serializer):
    pk_hostname = CharField()
    orderid = UUIDField(source="payment_uuid")
    obtain_datetime = DateTimeField(source="payment_date")

    def validate(self, attrs):
        return super().validate(attrs)
