"""Static views of the app."""
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from .mixins import LoginProhibitedMixin
from django.shortcuts import redirect
from django.urls import reverse
from main.models import *


class Home(LoginProhibitedMixin, TemplateView): # THE ORDER OF THESE SUPERCLASSES MATTERS
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN
    template_name = 'home.html'


class FeedView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        kwargs['current_user'] = self.request.user
        return render(request, 'feed.html', context=kwargs)
