from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from minutes.auth.models import Token, TokenTypes


class TokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        if len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    @staticmethod
    def authenticate_credentials(key):
        try:
            token = Token.objects.select_related('user').get(key=key, token_type=TokenTypes.AUTH)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        if token.expires < timezone.now():
            raise exceptions.AuthenticationFailed(_('Token expired'))
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        return token.user, token

    def authenticate_header(self, request):
        return self.keyword
