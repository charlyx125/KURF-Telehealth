from django.forms import Form
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from ..forms import *
from ..models import *
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = "users"


class StartChatView(LoginRequiredMixin, CreateView):
    model = Chat
    template_name = 'start_chat.html'
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.all()
        kwargs['current_user'] = self.request.user
        kwargs['create_chat_form'] = kwargs.get('create_chat_form', CreateChatForm(prefix="create_chat_form"))
        kwargs['create_message_form'] = kwargs.get('create_message_form', CreateMessageForm(prefix="create_message_form"))
        return kwargs

    def form_valid(self, form):
        """Process a valid form."""
        if isinstance(form, CreateChatForm):
            form.instance.first_user = form.cleaned_data.get('first_user')
            form.instance.second_user = User.objects.get(id=self.request.user.pk)
            self.kwargs['chat_instance'] = form.save()

        elif isinstance(form, CreateMessageForm):
            form.instance.chat = self.kwargs['chat_instance']
            form.instance.author = User.objects.get(id=self.request.user.pk)
            form.save()

    def check_chat_exists_in_db(self, chat_instance):
        return chat_instance.is_involved(self.request.user)

    def post(self, request, *args, **kwargs):
        chat_form = CreateChatForm(data=request.POST, prefix="create_chat_form")
        message_form = CreateMessageForm(data=request.POST, prefix="create_message_form")
        if chat_form.is_valid() and message_form.is_valid():
            self.form_valid(chat_form)
            if self.check_chat_exists_in_db(self.kwargs['chat_instance']):
                other_person_pk = self.kwargs['chat_instance'].get_other_user_in_chat(self.request.user)
                other_user = User.objects.get(id=other_person_pk)
                messages.add_message(self.request, messages.INFO, f"You have an existing chat with {other_user}")
            else:
                self.form_valid(message_form)
                messages.add_message(self.request, messages.SUCCESS, "Successful chat")
            # TODO: remove this message after implementing show chat view
            return redirect('user_list')
        else:
            messages.add_message(request, messages.INFO, "The details entered are not correct!")
            return self.render_to_response(
                self.get_context_data(create_chat_form=chat_form, create_message_form=message_form))


class ShowChatView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = "show_chat.html"
    pk_url_kwarg = 'chat_id'
    context_object_name = 'chat'

    def get_redirect_url(self):
        return 'user_list'


class ChatListView(LoginRequiredMixin, ListView):
    """View that shows all tickets directed to a staff/student"""
    template_name = "chat_list.html"
    queryset = "get_queryset"
    context_object_name = "chat"

    def get_queryset(self):
        queryset = Chat.objects.filter(Q(first_user__id=self.request.user.pk) | Q(second_user_id=self.request.user.pk)).values()
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['chat_list'] = self.get_queryset()
        return context
