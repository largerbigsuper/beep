from django.apps import AppConfig


class ActivityConfig(AppConfig):
    name = 'beep.activity'

    def ready(self):
        from . import signals
