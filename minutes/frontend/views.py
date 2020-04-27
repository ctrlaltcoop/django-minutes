from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.templatetags.static import static
from django.views.generic.base import View


class FrontendView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'minutes/frontend/index.html')
