import time
import json

from beep.wechat.models import mm_WxTemplate


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

    news_dict = {
        'name': '资讯更新提醒',
        'code': '7r6MUUipAu9ZIdNIYeP2NuOJNQZVmML344JeldvPmvI',
        'tpl_id': 2142,
        'vars_list': {
            '新闻标题': 'thing2',
            '更新时间': 'date4',
            '温馨提示': 'thing5'
        }
    }

    activity_dict = {
        'name': '活动开始提醒',
        'code': 'eCbhJnmIktj4OsnBZkJdaYeSdpC3ZuwI5vOdl70io50',
        'tpl_id': 731,
        'vars_list': {
            '活动名称': 'thing1',
            '活动时间': 'date2'
        }
    }
    
    prams_list = [news_dict, activity_dict]
    obj_list = []
    for p in prams_list:
        code = p.pop('code')
        obj, created = mm_WxTemplate.update_or_create(code=code, defaults=p)

@timeit
def run():
    init_wechat_template()


if __name__ == "__main__":
    run()
