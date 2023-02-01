from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.serializers import Serializer

from minutes.auth.models import Token, TokenTypes, user_retrieved_token


def create_new_token_set(user) -> dict:
    auth_token = Token.objects.create(
        user=user,
        token_type=TokenTypes.AUTH
    )
    refresh_token = Token.objects.create(
        user=user,
        token_type=TokenTypes.REFRESH
    )
    token_set = {
        'auth_token_key': auth_token.key,
        'auth_token_expires': auth_token.expires,
        'refresh_token_key': refresh_token.key,
        'refresh_token_expires': refresh_token.expires,
    }
    return token_set


class PasswordChangeSerializer(Serializer):  # pylint: disable=W0223
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class TokenSetSerializer(Serializer):  # pylint: disable=W0223
    auth_token_key = serializers.CharField(read_only=True)
    auth_token_expires = serializers.DateTimeField(read_only=True)
    refresh_token_key = serializers.CharField(read_only=True)
    refresh_token_expires = serializers.DateTimeField(read_only=True)

# pylint: disable-next=W0223
class TokenUserCredentialsSerializer(TokenSetSerializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        user_retrieved_token.send(sender=self.__class__, user=user)
        attrs.update(create_new_token_set(user))
        return attrs


class TokenRefreshSerializer(TokenSetSerializer):  # pylint: disable=W0223
    refresh_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        refresh_token_key = attrs.get('refresh_token')
        try:
            refresh_token = Token.objects.get(token_type=TokenTypes.REFRESH, key=refresh_token_key)
            if refresh_token.expires < timezone.now():
                raise serializers.ValidationError('Refresh token expired', code='expired_refresh_token')

        except Token.DoesNotExist as exc:
            raise serializers.ValidationError('Invalid refresh token', code='invalid_refresh_token') from exc

        user_retrieved_token.send(sender=self.__class__, user=refresh_token.user)
        attrs.update(create_new_token_set(refresh_token.user))
        return attrs


class TokenClaimSerializer(TokenSetSerializer):  # pylint: disable=W0223
    claim_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        claim_token_key = attrs.get('claim_token')
        try:
            claim_token = Token.objects.get(token_type=TokenTypes.CLAIM, key=claim_token_key)
            if claim_token.expires < timezone.now():
                raise serializers.ValidationError('Claim token expired', code='expired_claim_token')
        except Token.DoesNotExist as exc:
            raise serializers.ValidationError('Invalid claim token', code='invalid_claim_token') from exc
        user_retrieved_token.send(sender=self.__class__, user=claim_token.user)
        attrs.update(create_new_token_set(claim_token.user))
        claim_token.delete()
        return attrs
