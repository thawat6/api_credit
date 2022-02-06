from django.apps import AppConfig


class DataApiConfig(AppConfig):
    name = 'data_api'

    def ready(self):
        from . import signals
