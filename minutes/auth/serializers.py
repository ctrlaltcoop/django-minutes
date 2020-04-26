from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import Serializer

from minutes.auth.models import Token, TokenTypes


class PasswordChangeSerializer(Serializer):  # pylint: disable=W0223
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class TokenSetSerializer(Serializer):  # pylint: disable=W0223
    auth_token_key = serializers.CharField()
    auth_token_expires = serializers.DateTimeField()
    refresh_token_key = serializers.CharField()
    refresh_token_expires = serializers.DateTimeField()


class TokenRefreshSerializer(Serializer):  # pylint: disable=W0223
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh_token_key = attrs.get('refresh_token')
        try:
            refresh_token = Token.objects.get(token_type=TokenTypes.REFRESH, key=refresh_token_key)
            if refresh_token.expires <= timezone.now():
                raise serializers.ValidationError('Refresh token expired', code='expired_refresh_token')

        except Token.DoesNotExist:
            raise serializers.ValidationError('Invalid refresh token', code='invalid_refresh_token')
        return attrs
