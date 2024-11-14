from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.vending.models import Place
from apps.vending.serializers import PlaceSerializer
from apps.account.models import BaseSubscription, SubscriptionPayment
from apps.account.tasks import apply_user_subscription_payment

from core.pagination import PageNumberSetPagination


class PlaceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceSerializer
    pagination_class = PageNumberSetPagination

    def get_queryset(self):
        return Place.objects.all()

    @action(methods=["post"], detail=True)
    def subscribe(self, request, *args, **kwargs):
        place = self.get_object()
        user = request.user

        base_subscription = BaseSubscription.objects.first()
        if not base_subscription:
            raise ValueError("Подписка не существует")

        payment = SubscriptionPayment.objects.create(
            user=user, place=place, price=base_subscription.price
        )

        # TODO: логика оплаты
        apply_user_subscription_payment.delay(payment_id=payment.id)

        return Response(status=201)
