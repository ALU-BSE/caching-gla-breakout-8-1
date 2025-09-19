from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer


def get_cache_key(prefix, identifier=None):
    if identifier:
        return f"{prefix}_{identifier}"
    return prefix


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        cache_key = get_cache_key('user_list')

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)

        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)

        return response