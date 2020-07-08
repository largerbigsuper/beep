from django.db.models.manager import Manager
from django.core.cache import cache
from django.db.models import F

class CacheKey(object):

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
    TIME_OUT_WXID_SET = 60 * 60 * 24 * 365


class StatsUtils:

    def _update_stats(self, pk, field_name, amount=1):
        if amount > 0:
            value = F(field_name) + amount
        else:
            value = F(field_name) - abs(amount)
        updates = {
            field_name: value
        }
        self.filter(pk=pk).update(**updates)
    
    def increase(self, pk, field_name, amount=1):
        return self._update_stats(pk, field_name, amount)

    def decrease(self, pk, field_name, amount=1):
        amount = ~amount + 1
        return self._update_stats(pk, field_name, amount)

class ModelManager(Manager, CacheKey, StatsUtils):
    
    cache = cache
