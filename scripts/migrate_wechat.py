from beep.wechat.models import mm_WxTemplate
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


@timeit
def init_wechat_template():
    """统计话题博文总量
    """

    p1 = {
        'name': '资讯更新提醒',
        'code': '7r6MUUipAu9ZIdNIYeP2NoWCeYX0ksjOAvtMTmrFH9U',
        'vars_list': ['thing2', 'thing3', 'date4', 'thing5']
    }

    p2 = {
        'name': '活动开始提醒',
        'code': 'eCbhJnmIktj4OsnBZkJdaYeSdpC3ZuwI5vOdl70io50',
        'vars_list': ['thing1', 'date2']
    }
    prams_list = [p1, p2]
    obj_list = []
    for p in prams_list:
        obj = mm_WxTemplate.model(**p)
        obj_list.append(obj)

    mm_WxTemplate.bulk_create(obj_list)


@timeit
def run():
    init_wechat_template()


if __name__ == "__main__":
    run()
