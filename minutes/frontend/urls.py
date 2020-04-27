from django.conf import settings
from django.conf.urls import url
from django.urls import path

from minutes.frontend.views import FrontendView


urlpatterns = [
    path('app/', FrontendView.as_view()),
]
