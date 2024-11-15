from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.vending.models import Place
from apps.vending.serializers import PlaceSerializer, SubscriptionTariffSerializer

from core.pagination import PageNumberSetPagination


class PlaceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceSerializer
    pagination_class = PageNumberSetPagination

    def get_queryset(self):
        return Place.objects.filter(is_active=True)

    @action(methods=["get"], detail=True)
    def tariffs(self, request, *args, **kwargs):
        place = self.get_object()
        serializer = SubscriptionTariffSerializer(
            place.tariffs.filter(is_active=True),
            many=True,
            context=self.get_serializer_context(),
        )
        return Response(serializer.data, status=200)
