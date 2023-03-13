from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import authentication


class DrfAuthBackend(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'').split()

        if len(auth) < 2:
            return None
        try:
            return (get_user_model().objects.get(username=auth[1]), None)
        except User.DoesNotExist:
            return None
