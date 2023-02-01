from django.apps import AppConfig
from django.conf import settings


class MinutesAuthConfig(AppConfig):
    label = 'minutes_auth'
    name = 'minutes.auth'

    MINUTES_AUTH_TOKEN_EXPIRES_IN = getattr(settings, 'MINUTES_AUTH_TOKEN_EXPIRES_IN', 3600)
    MINUTES_REFRESH_TOKEN_EXPIRES_IN = getattr(settings, 'MINUTES_REFRESH_TOKEN_EXPIRES_IN', 86400)
