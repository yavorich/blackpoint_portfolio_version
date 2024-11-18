from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.vending.models import DrinkHistory
from apps.vending.serializers import DrinkHistorySerializer


class DrinkHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DrinkHistorySerializer

    def get_queryset(self):
        return DrinkHistory.objects.filter(user=self.request.user).order_by(
            "-purchased_at"
        )
