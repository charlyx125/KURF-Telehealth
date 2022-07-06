"""View mixins."""
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from telehealth import settings
from ..models import *
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""
    login_url = settings.LOGIN_URL
    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class UserInvolvedInChatOnly(UserPassesTestMixin):
    redirect_result = False

    """override this function to change the redirect_url"""
    def get_redirect_url(self):
        return 'chat_list'

    def test_func(self):
        try:
            chat = self.get_object()
        except Http404:
            messages.add_message(self.request, messages.INFO, 'Please select a different chat')
            return redirect(self.get_redirect_url())
        else:
            return Chat.is_involved(chat, self.request.user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect(self.get_redirect_url())
        else:
            return redirect('log_in')
