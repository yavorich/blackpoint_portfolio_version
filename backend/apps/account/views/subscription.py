from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.account.serializers import (
    UserSubscriptionSerializer,
    SubscriptionPaymentSerializer,
)
from apps.account.tasks import apply_user_subscription_payment

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
            return SubscriptionPaymentSerializer
        return UserSubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        # TODO: логика оплаты
        apply_user_subscription_payment.apply_async(args=[payment.id], countdown=3)
        return Response(status=201)


# class SubscriptionTariffView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = SubscriptionTariffSerializer
#     queryset = SubscriptionTariff.objects.all()
