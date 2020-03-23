from beep.cfg.models import mm_ActionPointCfg
from beep.users.models import mm_Point


def clear():
    mm_ActionPointCfg.all().delete()

def init_action_point_cfg():
    """初始化配置表
    """
    cfg_list = []
    for code, name in mm_Point.ACTION_CHOICE:
        cfg = mm_ActionPointCfg.model(code=code, name=name, point=10)
        cfg_list.append(cfg)

    mm_ActionPointCfg.bulk_create(cfg_list)


def run():
    clear()
    init_action_point_cfg()

