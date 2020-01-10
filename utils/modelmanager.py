from django.db.models.manager import Manager
from django.core.cache import cache

class CacheKey(object):

    key_live_rooms = 'live_rooms'
    key_user_info = 'user_{}'
    key_wxid_set = 'wxid_set'
    key_user_first_comment_everyday = 'user_{}_comment'
    TIME_OUT_USER_INFO = 60 * 60 * 24
    TIME_OUT_WXID_SET = 60 * 60 * 1

class ModelManager(Manager, CacheKey):
    
    cache = cache
