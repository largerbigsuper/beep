from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'beep.users'

    def ready(self):
        from . import signals