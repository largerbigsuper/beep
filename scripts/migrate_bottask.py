from beep.bot.models import mm_BotTask

def run():
    bot_task_names = [
        'task_add_blog_comment',
        'task_add_blog_like',
        'task_add_blog_forward',
        'task_add_activity_commnet',
        'task_add_user_following',
    ]
    for name in bot_task_names:
        mm_BotTask.get_or_create(name=name, is_open=False)
        print('add {} done'.format(name))
