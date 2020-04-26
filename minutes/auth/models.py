from enum import Enum


from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import IntegerField, ForeignKey, IntegerChoices
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token as BaseToken

app_conf = apps.get_app_config('minutes.auth')


class TokenTypes(IntegerChoices):
    REFRESH = 0
    AUTH = 1


# Create your models here.
class Token(BaseToken):
    token_type = IntegerField(choices=TokenTypes.choices)
    expires = models.DateTimeField()
    user = ForeignKey(settings.AUTH_USER_MODEL, related_name='tokens',
                      on_delete=models.CASCADE, verbose_name=_('User'))
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.expires:
            expiry_time = timezone.timedelta(seconds=app_conf.MINUTES_REFRESH_TOKEN_EXPIRES_IN) \
                if self.token_type == TokenTypes.REFRESH \
                else timezone.timedelta(seconds=app_conf.MINUTES_AUTH_TOKEN_EXPIRES_IN)
            self.expires = timezone.now() + expiry_time
        return super().save(*args, **kwargs)
