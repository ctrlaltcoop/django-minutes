from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer as UserCredentialsSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from minutes.auth.models import Token, TokenTypes
from minutes.auth.serializers import TokenRefreshSerializer, TokenSetSerializer
from minutes.auth.serializers import PasswordChangeSerializer


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


class PasswordChangeViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def create(self, request):
        serializer: PasswordChangeSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.data['old_password']):
            raise PermissionDenied('Old password not correct')
        request.user.set_password(serializer.data['new_password'])
        request.user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class TokenViewSet(GenericViewSet):
    serializer_class = TokenSetSerializer

    def create(self, request):
        serializer: UserCredentialsSerializer = UserCredentialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_set_serializer = self.get_serializer(
            data=create_new_token_set(User.objects.get(username=serializer.data['username']))
        )
        token_set_serializer.is_valid()
        return Response(token_set_serializer.data, status=status.HTTP_201_CREATED)


class TokenRefreshViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenSetSerializer

    def create(self, request):
        serializer: TokenRefreshSerializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = Token.objects.get(key=serializer.data['refresh_token']).user
        token_set_serializer = self.get_serializer(
            data=create_new_token_set(user)
        )
        token_set_serializer.is_valid()
        return Response(token_set_serializer.data, status=status.HTTP_201_CREATED)
