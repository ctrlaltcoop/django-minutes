from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from minutes.auth.apps import MinutesAuthConfig
from minutes.auth.api import PasswordChangeViewSet, TokenUserCredentialsViewSet, TokenRefreshViewSet, TokenClaimViewSet, \
    InvitationViewSet
from minutes.api import MeetingSeriesViewSet, UserViewSet, AgendaItemViewSet, AgendaSubItemViewSet, DecisionViewSet, \
    MeetingViewSet, VoteChoiceViewSet, AnonymousVoteViewSet, RollCallVoteViewSet

viewset_router = DefaultRouter()

viewset_router.register('users', UserViewSet)
viewset_router.register('meetingseries', MeetingSeriesViewSet)
viewset_router.register('meeting', MeetingViewSet)
viewset_router.register('agendaitem', AgendaItemViewSet, basename='agendaitem')
viewset_router.register('agendasubitem', AgendaSubItemViewSet, basename='subitem')
viewset_router.register('decision', DecisionViewSet, basename='decision')
viewset_router.register('anonymousvote', AnonymousVoteViewSet, basename='anonymousvote')
viewset_router.register('rollcallvote', RollCallVoteViewSet, basename='rollcallvote')
viewset_router.register('votechoice', VoteChoiceViewSet, basename='votechoice')

if MinutesAuthConfig.name in settings.INSTALLED_APPS:
    viewset_router.register('invitation', InvitationViewSet, basename='invitation')
    viewset_router.register('changepassword', PasswordChangeViewSet, basename='passwordchange')
    viewset_router.register('token', TokenUserCredentialsViewSet, basename='token')
    viewset_router.register('token-refresh', TokenRefreshViewSet, basename='tokenrefresh')
    viewset_router.register('token-claim', TokenClaimViewSet, basename='tokenclaim')


schema_patterns = [
    path('api/v1/', include(viewset_router.urls))
]

urlpatterns = [
    path('api/v1/openapi/', get_schema_view(
        title="Minutes API",
        description="Minutes API",
        version="1.0.0",
        patterns=schema_patterns,
        public=True,
        permission_classes=[AllowAny]
    ), name='openapi-schema'),
    path('api/v1/docs/', TemplateView.as_view(
        template_name='minutes/redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),

    path('', include('minutes.frontend.urls'))
] + schema_patterns
