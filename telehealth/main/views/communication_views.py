from django.forms import Form
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from ..forms import *
from ..models import *
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from ..views.mixins import *


class StartChatView(LoginRequiredMixin, CreateView):
    model = Chat
    template_name = 'start_chat.html'
    http_method_names = ['get', 'post']

    def get_users_with_existing_chats_with_current_user(self):
        current_user = self.request.user
        chats_received = current_user.chats_received.all()
        chats_sent = current_user.chats_started.all()
        chats = chats_received.union(chats_sent)
        chats = list(chats)
        for i in range(len(chats)):
            other_user_in_chat = chats[i].get_other_user_in_chat(current_user)
            chats[i] = other_user_in_chat
        return chats

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.all()
        kwargs['current_user'] = self.request.user
        kwargs['create_chat_form'] = kwargs.get('create_chat_form', CreateChatForm(prefix="create_chat_form"))
        ######
        # The user is only able to chat with users they have not had a chat before.
        # The user is not able to chat with themselves.
        existing_chats = self.get_users_with_existing_chats_with_current_user()
        kwargs['create_chat_form'].fields['first_user'].queryset = User.objects.exclude(id__in=existing_chats).exclude(id=self.request.user.pk)
        ######
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
        current_user = request.user
        chat_form = CreateChatForm(data=request.POST, prefix="create_chat_form")
        message_form = CreateMessageForm(data=request.POST, prefix="create_message_form")
        if chat_form.is_valid() and message_form.is_valid():
            self.form_valid(chat_form)
            chat = self.kwargs['chat_instance']
            self.form_valid(message_form)
            messages.add_message(self.request, messages.SUCCESS, "Successful chat")
            return redirect(f'/show_chat/{chat.id}')
        else:
            messages.add_message(request, messages.INFO, "The details entered are not correct!")
            return self.render_to_response(
                self.get_context_data(create_chat_form=chat_form, create_message_form=message_form))


class ShowChatView(LoginRequiredMixin, UserInvolvedInChatOnly, DetailView):
    model = Chat
    template_name = "show_chat.html"
    pk_url_kwarg = 'chat_id'
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""
        kwargs['chat'] = self.get_object()
        kwargs['chat_messages'] = kwargs['chat'].messages_in_this_chat.all()
        kwargs['current_user'] = self.request.user
        kwargs['form'] = CreateMessageForm()
        return kwargs


class ReplyChatView(LoginRequiredMixin, UserInvolvedInChatOnly, CreateView):
    model = Message
    pk_url_kwarg = 'chat_id'
    form_class = CreateMessageForm
    queryset = Chat.objects.all()
    context_object_name = 'chat'
    template_name = "show_chat.html"

    def get_context_data(self, **kwargs):
        kwargs['chat'] = self.get_object()
        kwargs['current_user'] = self.request.user
        kwargs['form'] = CreateMessageForm()
        return kwargs

    def form_valid(self, form):
        form.instance.chat = self.get_object()
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_chat', kwargs={'chat_id': self.get_object().pk})


class ChatListView(LoginRequiredMixin, ListView):
    """View that shows all tickets directed to a staff/student"""
    template_name = "chat_list.html"
    queryset = "get_queryset"
    context_object_name = "chat"

    def get_queryset(self):
        queryset = Chat.objects.filter(Q(first_user=self.request.user) | Q(second_user=self.request.user))
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        """Generate context data to be shown in the template."""
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['chat_list'] = self.get_queryset()
        return context
