from rest_framework.serializers import ModelSerializer

from apps.account.models import Document


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ["file"]
