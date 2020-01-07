from beep.cfg.models import mm_ActionPointCfg
from beep.users.models import mm_Point

def init_action_point_cfg():
    """初始化配置表
    """
    cfg_list = []
    for code, name in mm_Point.ACTION_CHOICE:
        cfg = mm_ActionPointCfg.model(code=code, name=name)
        cfg_list.append(cfg)

    mm_ActionPointCfg.bulk_create(cfg_list)


def run():
    init_action_point_cfg()

