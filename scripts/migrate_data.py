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
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed

#
from django.db.models import Count

from beep.blog.models import mm_Blog, mm_Topic


def migrate_topic__total_blog():
    """统计话题博文总量
    """
    data_list = mm_Blog.filter(topic_id__gt=0).values_list('topic').annotate(total_blog=Count('topic')).order_by('topic')
    data_dict = dict(data_list)
    for pk, count in data_dict.items():
        mm_Topic.filter(pk=pk).update(total_blog=count)

@timeit
def run():
    migrate_topic__total_blog()


if __name__ == "__main__":
    run()