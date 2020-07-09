import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%s  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed

#
from django.db.models import Count, Sum

from beep.blog.models import mm_Blog, mm_Topic
from beep.users.models import mm_User, mm_RelationShip

@timeit
def migrate_topic__total_blog():
    """统计话题博文总量
    """
    data_list = mm_Blog.filter(topic_id__gt=0).values_list('topic').annotate(total_blog=Count('topic')).order_by('topic')
    data_dict = dict(data_list)
    for pk, count in data_dict.items():
        mm_Topic.filter(pk=pk).update(total_blog=count)

@timeit
def migrate_user__total_blog():
    """同步用户博文数
    """
    data_list = mm_Blog.filter(user_id__gt=0).values_list('user').annotate(total_blog=Count('user')).order_by('user')
    data_dict = dict(data_list)
    for pk, count in data_dict.items():
        mm_User.filter(pk=pk).update(total_blog=count)

@timeit
def migrate_user__total_following():
    """同步用户关注数
    """
    following_list = mm_RelationShip.values_list('user').annotate(total=Count('id')).order_by()
    following_dict = dict(list(following_list))
    for pk, count in following_dict.items():
        mm_User.filter(pk=pk).update(total_following=count)


@timeit
def migrate_user__total_followers():
    """同步用户粉丝数
    """
    followers_list = mm_RelationShip.values_list('following').annotate(total=Count('id')).order_by()
    followers_dict = dict(list(followers_list))
    for pk, count in followers_dict.items():
        mm_User.filter(pk=pk).update(total_followers=count)


@timeit
def run():
    # migrate_topic__total_blog()
    migrate_user__total_blog()
    migrate_user__total_following()
    migrate_user__total_followers()



if __name__ == "__main__":
    run()