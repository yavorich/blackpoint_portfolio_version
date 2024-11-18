from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.account.models import Document
from apps.account.serializers import DocumentSerializer


class DocumentAPIView(RetrieveAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(Document, type=self.kwargs.get("type"))
