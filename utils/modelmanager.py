from django.db.models.manager import Manager
from django.core.cache import cache

class CacheKey(object):

    key_live_rooms = 'live_rooms'

class ModelManager(Manager, CacheKey):
    
    cache = cache
