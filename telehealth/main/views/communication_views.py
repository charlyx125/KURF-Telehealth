from django.forms import Form
from django.views import View
from django.views.generic import CreateView, DetailView
from main.forms import *
from main.models import *
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class ShowChatView(LoginRequiredMixin, DetailView):
    """View that shows individual ticket contents"""
    model = Chat
    template_name = "Show-Ticket.html"
    pk_url_kwarg = 'ticket_id'
    context_object_name = 'ticket'

    def get_redirect_url(self):
        return 'ticket-list'

    def get(self, request, *args, **kwargs):
        """Handle get request, and redirect to ticket-list if ticket_id invalid."""
        try:
            object = self.get_object()
        except Http404:
            return redirect(self.get_redirect_url())
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""
        kwargs['object'] = self.get_object()
        kwargs['current_user'] = self.request.user
        kwargs['form'] = CreateMessageForm()
        kwargs['anonymous_username'] = ANONYMOUS_USERNAME
        kwargs['anonymous'] = kwargs['object'].anonymous
        kwargs['student'] = kwargs['object'].student


# class ReplyChatView(LoginRequiredMixin, CreateView):
#     model = Message
#     form_class = CreateMessageForm
#     queryset = Ticket.objects.all()
#     context_object_name = 'ticket'
#     template_name = "Show-Ticket.html"
#
#     def get_context_data(self, **kwargs):
#         kwargs['object'] = self.get_object()
#         kwargs['current_user'] = self.request.user
#         kwargs['form'] = CreateMessageForm()
#         return kwargs
#
#     def form_valid(self, form):
#         form.instance.ticket = self.get_object()
#         form.instance.author = self.request.user
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('show-ticket', kwargs={'ticket_id': self.get_object().pk})
