from django.apps import AppConfig


class TodoappConfig(AppConfig):
    name = 'todoapp'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import todoapp.signals
