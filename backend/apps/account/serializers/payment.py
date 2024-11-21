from rest_framework.serializers import (
    Serializer,
    CharField,
    DateTimeField,
    UUIDField,
    URLField,
)


class PaymentWebhookSerializer(Serializer):
    pk_hostname = CharField()
    orderid = UUIDField(source="payment_uuid")
    obtain_datetime = DateTimeField(source="payment_date")

    def validate(self, attrs):
        return super().validate(attrs)


class PaymentResponseSerializer(Serializer):
    invoice_id = CharField()
    payment_url = URLField()
    expiry_datetime = DateTimeField()
