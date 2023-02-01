from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from minutes.auth.models import Invitation
from minutes.auth.serializers import TokenRefreshSerializer, \
    TokenUserCredentialsSerializer, TokenClaimSerializer
from minutes.auth.serializers import PasswordChangeSerializer
from minutes.serializers import InvitationRequestSerializer, FullUserSerializer


class PasswordChangeViewSet(GenericViewSet):
    schema = AutoSchema(tags=['auth'])
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
    def create(self, request):
        serializer: TokenUserCredentialsSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenUserCredentialsViewSet(TokenViewSet):
    schema = AutoSchema(operation_id_base="TokenSetByCredentials", tags=['auth'])
    serializer_class = TokenUserCredentialsSerializer


class TokenRefreshViewSet(TokenViewSet):
    schema = AutoSchema(operation_id_base="TokenSetByRefresh", tags=['auth'])
    serializer_class = TokenRefreshSerializer


class TokenClaimViewSet(TokenViewSet):
    serializer_class = TokenClaimSerializer
    schema = AutoSchema(operation_id_base="TokenSetByClaim", tags=['auth'])


class InvitationViewSet(GenericViewSet):
    schema = AutoSchema(tags=['auth'])
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
        user_serializer = FullUserSerializer(instance=new_user)
        return Response(user_serializer.data, status=HTTP_201_CREATED)
