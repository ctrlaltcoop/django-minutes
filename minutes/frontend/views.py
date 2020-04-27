from django.shortcuts import render
from django.views.generic.base import View


class FrontendView(View):
    def get(self, request):
        return render(request, 'minutes/frontend/index.html')
