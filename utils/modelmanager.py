from django.db.models.manager import Manager
from django.core.cache import cache

class CacheKey(object):

    key_live_rooms = 'live_rooms'
    key_user_info = 'user_{}'
    key_wxid_set = 'wxid_set'
    key_live_rooms_activity_map = 'live_rooms_map'
    """微信群和活动直播id映射
    {
        "wxid": {"activity_id_1", "activity_id_2"}
    }
    """
    key_user_first_comment_everyday = 'user_{}_comment'
    TIME_OUT_USER_INFO = 60 * 60 * 24
    TIME_OUT_WXID_SET = 60 * 60 * 1

class ModelManager(Manager, CacheKey):
    
    cache = cache
