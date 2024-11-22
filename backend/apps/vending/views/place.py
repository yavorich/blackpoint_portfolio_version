from django.utils.timezone import localdate
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.account.models import UserSubscription
from apps.vending.models import Place, DrinkType
from apps.vending.serializers import (
    PlaceSerializer,
    DrinkTypeSerializer,
    DrinkVolumeSerializer,
    DrinkBuySerializer,
)
from apps.vending.tasks import add_credits_to_terminal

from core.pagination import PageNumberSetPagination


class PlaceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceSerializer
    pagination_class = PageNumberSetPagination

    def get_queryset(self):
        return Place.objects.filter(is_active=True)

    @action(methods=["get"], detail=True, url_path="drinks")
    def drinks(self, request, pk=None):
        place = self.get_object()
        drink_types = DrinkType.objects.filter(
            volumes__in=place.drinks.all()
        ).distinct()
        serializer = DrinkTypeSerializer(drink_types, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        url_path="drinks/(?P<drink_type_id>[^/.]+)/volumes",
    )
    def drink_volumes(self, request, pk=None, drink_type_id=None):
        """Список DrinkVolume для выбранного DrinkType"""
        place = self.get_object()
        volumes = place.drinks.filter(drink_type_id=drink_type_id)
        serializer = DrinkVolumeSerializer(volumes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def buy(self, request, pk=None):
        place = self.get_object()
        subscription = UserSubscription.objects.filter(
            user=request.user,
            place=place,
            start_date__lte=localdate(),
            expire_date__gte=localdate(),
        ).first()
        if not subscription:
            raise ValidationError(
                "У вас нет активного абонемента для покупки в этом автомате"
            )
        elif subscription.today_cups <= 0:
            raise ValidationError(
                "Вы уже заказали доступное кол-во напитков по абонементу на сегодня"
            )
        serializer = DrinkBuySerializer(
            data=request.data, context={"place": place, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        subscription.today_cups -= 1
        subscription.save()

        add_credits_to_terminal.delay(
            place.terminal_id, serializer.validated_data["drink"].price
        )

        return Response(serializer.data, status=201)
