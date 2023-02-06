import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from django.conf import settings


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print(request.headers)
        username = request.headers.get("trust-me")
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed(f"no user:{username}")


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("jwt")
        if not token:
            return None

        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("Invalid token")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("user not found")
