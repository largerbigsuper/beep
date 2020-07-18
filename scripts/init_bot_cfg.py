from beep.bot.models import mm_BotSetting

def run():
    settting_tuples = [
        ('blog_comment_min_count', '2', '博文评论最小次数'),
        ('blog_comment_max_count', '8', '博文评论最大次数'),
        ('blog_like_min_count', '10', '博文点赞最小次数'),
        ('blog_like_max_count', '70', '博文点赞最大次数'),
        ('blog_forward_min_count', '1', '博文转发最小次数'),
        ('blog_forward_max_count', '2', '博文转发最大次数'),
    ]

    objs = []
    for t in settting_tuples:
        obj = mm_BotSetting.model(name=t[0].upper(), value=t[1], desc=t[2])
        objs.append(obj)
    mm_BotSetting.bulk_create(objs)
