from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.account.serializers import (
    UserSubscriptionSerializer,
    BuySubscriptionSerializer,
    PaymentResponseSerializer,
)
from apps.account.services.payment_manager import PaymentManager

from core.pagination import PageNumberSetPagination


class UserSubscriptionViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberSetPagination

    def get_queryset(self):
        return self.request.user.user_subscriptions.all()

    def get_serializer_class(self):
        if self.action == "create":
            return BuySubscriptionSerializer
        return UserSubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        user.email = validated_data["email"]
        user.phone = validated_data["phone"]
        user.save()

        payment_data = PaymentManager().buy(validated_data, user=user)
        response_serializer = PaymentResponseSerializer(payment_data)
        return Response(response_serializer.data, status=201)


# class SubscriptionTariffView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = SubscriptionTariffSerializer
#     queryset = SubscriptionTariff.objects.all()
