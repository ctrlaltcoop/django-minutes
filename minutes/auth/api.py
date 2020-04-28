from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer as UserCredentialsSerializer
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from minutes.auth.models import Token, TokenTypes, Invitation
from minutes.auth.serializers import TokenRefreshSerializer, TokenSetSerializer, ClaimSerializer
from minutes.auth.serializers import PasswordChangeSerializer
from minutes.schema import MinutesSchema
from minutes.serializers import InvitationRequestSerializer, UserSerializer


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
    schema = MinutesSchema(tags=['auth'])
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
    schema = MinutesSchema(operation_id_base="TokenSetByCredentials", tags=['auth'])

    def create(self, request):
        serializer: UserCredentialsSerializer = UserCredentialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_set_serializer = self.get_serializer(
            data=create_new_token_set(serializer.validated_data['user'])
        )
        token_set_serializer.is_valid()
        return Response(token_set_serializer.validated_data, status=status.HTTP_201_CREATED)


class TokenRefreshViewSet(GenericViewSet):
    schema = MinutesSchema(operation_id_base="TokenSetByRefresh", tags=['auth'])
    serializer_class = TokenSetSerializer

    def create(self, request):
        serializer: TokenRefreshSerializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = Token.objects.get(key=serializer.validated_data['refresh_token']).user
        token_set_serializer = self.get_serializer(
            data=create_new_token_set(user)
        )
        token_set_serializer.is_valid()
        return Response(token_set_serializer.validated_data, status=status.HTTP_201_CREATED)


class TokenClaimViewSet(GenericViewSet):
    serializer_class = TokenSetSerializer
    schema = MinutesSchema(operation_id_base="TokenSetByClaim", tags=['auth'])

    def create(self, request):
        serializer: ClaimSerializer = ClaimSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = Token.objects.get(key=serializer.validated_data['claim_token'])
        user = token.user
        token.delete()
        token_set_serializer = self.get_serializer(
            data=create_new_token_set(user)
        )
        token_set_serializer.is_valid()
        return Response(token_set_serializer.validated_data, status=status.HTTP_201_CREATED)


class InvitationViewSet(GenericViewSet):
    schema = MinutesSchema(tags=['auth'])
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = InvitationRequestSerializer

    def create(self, request):
        invitation_request = InvitationRequestSerializer(data=request.data)
        invitation_request.is_valid(raise_exception=True)
        if User.objects.filter(email=invitation_request.data['email']).exists():
            raise ValidationError('A user with this email address already exists')
        new_user = User.objects.create(
            username=invitation_request.validated_data['username'],
            email=invitation_request.validated_data['email']
        )
        Invitation.objects.create(
            invited_user=new_user,
            inviting_user=request.user,
        )
        user_serializer = UserSerializer(instance=new_user)
        return Response(user_serializer.data, status=HTTP_201_CREATED)
