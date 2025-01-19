from django.core.cache import cache

from mailout.models import Clients
from config.settings import CACHE_ENABLED


def get_clients_from_cache():
    """Получает данные о получателях рассылки из кэша. Если кэш пуст, получает данные из бд"""

    if not CACHE_ENABLED:
        return Clients.objects.all()

    key = 'clients'

    client = cache.get(key)

    if client is not None:
        return client

    client = Clients.objects.all()
    cache.set(key, client, 60 * 15)
    return client
