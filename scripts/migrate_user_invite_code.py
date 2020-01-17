import time
import json

import shortuuid

from beep.users.models import mm_User


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

@timeit
def generate_invite_code():
    for u in mm_User.all():
        u.invite_code = shortuuid.ShortUUID().random(length=6)
        u.save(update_fields=['invite_code'])

@timeit
def run():
    generate_invite_code()

if __name__ == "__main__":
    run()