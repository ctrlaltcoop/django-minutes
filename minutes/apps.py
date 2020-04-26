from django.apps import AppConfig
from django.conf import settings


class MinutesConfig(AppConfig):
    name = 'minutes'

    MINUTES_INSTANCE_NAME = getattr(settings, 'MINUTES_INSTANCE_NAME', 'A minutes instance')
