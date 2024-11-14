from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.support.serializers import SupportRequestSerializer


class SupportRequestView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupportRequestSerializer
