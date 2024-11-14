from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.account.serializers import UserSubscriptionsSerializer
from apps.account.models import SubscriptionPayment, BaseSubscription
from apps.account.tasks import apply_user_subscription_payment

from core.pagination import PageNumberSetPagination


class UserSubscriptionViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSubscriptionsSerializer
    pagination_class = PageNumberSetPagination

    def get_queryset(self):
        return self.request.user.user_subscriptions.all()

    @action(methods=["post"], detail=True)
    def renew(self, request, *args, **kwargs):
        subscription = self.get_object()
        base_subscription = BaseSubscription.objects.first()
        if not base_subscription:
            raise ValueError("Подписка не существует")

        payment = SubscriptionPayment.objects.create(
            user=subscription.user,
            place=subscription.place,
            price=base_subscription.price,
        )

        # TODO: логика оплаты
        apply_user_subscription_payment.delay(payment_id=payment.id)

        return Response(status=201)
