import uuid
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class UUIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        raw_uuid = auth_header.strip()

        try:
            user_uuid = uuid.UUID(raw_uuid, version=4)
        except ValueError:
            raise AuthenticationFailed("Invalid UUID format.")

        try:
            user = User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            raise AuthenticationFailed("No user with the provided UUID.")

        return (user, None)
