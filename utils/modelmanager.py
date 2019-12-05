from django.db.models.manager import Manager
from django.core.cache import cache

class CacheKey(object):

    key_live_rooms = 'live_rooms'
    key_user_info = 'user_{}'
    TIME_OUT_USER_INFO = 60 * 60 * 24

class ModelManager(Manager, CacheKey):
    
    cache = cache
