from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'beep.blog'

    def ready(self):
        from . import signals
