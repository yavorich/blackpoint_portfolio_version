from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.account.serializers import PaymentWebhookSerializer
from apps.account.models import SubscriptionPayment
from apps.account.tasks import confirm_user_subscription_payment


class PaymentWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        payment = get_object_or_404(
            SubscriptionPayment,
            uuid=validated_data["payment_uuid"],
            status=SubscriptionPayment.Status.PENDING,
        )

        payment.status = SubscriptionPayment.Status.SUCCESS
        payment.payment_date = validated_data["payment_date"]
        payment.save()

        confirm_user_subscription_payment.delay(payment.uuid)

        return Response(status=201)
