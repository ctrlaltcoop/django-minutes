from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import IntegerField, ForeignKey, IntegerChoices, CASCADE
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token as BaseToken

from minutes.apps import MinutesConfig

app_conf = apps.get_app_config('minutes.auth')


class TokenTypes(IntegerChoices):
    REFRESH = 0
    AUTH = 1
    CLAIM = 2


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


class Invitation(models.Model):
    inviting_user = models.ForeignKey(User, on_delete=CASCADE, related_name='invites_sent')
    invited_user = models.ForeignKey(User, on_delete=CASCADE, related_name='invites')

    def save(self, **kwargs):
        super().save(**kwargs)
        invite_mail = render_to_string('minutes/mails/invitation.txt', {
            'invited_user': self.invited_user,
            'inviting_user': self.inviting_user,
            'instance_name': MinutesConfig.MINUTES_INSTANCE_NAME,
            'invitation_url': 'tbd'  # TODO: Fill once FE urls can be resolved
        })
        self.invited_user.email_user(_('You were invited to collaborate on meeting minutes'), invite_mail)
