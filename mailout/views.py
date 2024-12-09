from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.urls import reverse_lazy

from . import models
from .forms import ClientsForm, MessageForm, MailoutForm
from .models import Home, Clients, Message, Mailout
from .services import get_clients_for_mailout


class HomeListView(ListView):
    model = Home
    template_name = 'mailout/home.html'
    context_object_name = 'home'

    def get_queryset(self):
        queryset = Clients.objects.filter().distinct().count()
        return queryset


class ClientsCreateView(CreateView):
    model = Clients
    form_class = ClientsForm
    template_name = 'mailout/clients.html'
    success_url = reverse_lazy('mailout:clients')

    def form_valid(self, form):
        clients = form.save()
        user = self.request.user
        clients.owner = user
        clients.save()
        return super().form_valid(form)


class ClientsListView(ListView):
    model = Clients
    template_name = 'mailout/clients.html'
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        context = super(ClientsListView, self).get_context_data(**kwargs)
        context['form'] = ClientsForm()
        return context


class ClientsDetailView(DetailView):
    model = Clients
    template_name = 'mailout/client_view.html'
    context_object_name = 'client'


class ClientsUpdateView(UpdateView):
    model = Clients
    form_class = ClientsForm
    template_name = 'mailout/clients.html'
    success_url = reverse_lazy('mailout:clients')


class ClientsDeleteView(DeleteView):
    model = Clients
    success_url = reverse_lazy('mailout:clients')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailout/messages.html'
    success_url = reverse_lazy('mailout:message')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message
    template_name = 'mailout/messages.html'
    context_object_name = 'messages'

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context['form'] = MessageForm()
        return context


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailout/message_view.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailout/messages.html'
    success_url = reverse_lazy('mailout:message')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailout:message')


class MailoutCreateView(CreateView):
    model = Mailout
    form_class = MailoutForm
    template_name = 'mailout/mailout.html'
    success_url = reverse_lazy('mailout:mailout')

    def form_valid(self, form):
        mailout = form.save()
        user = self.request.user
        mailout.owner = user
        if mailout.status == 'Завершена':
            mailout.sent_at(auto_now_add=True)

        if mailout.status == 'Запущена':
            mailout.is_active = True

        mailout.save()

        return super().form_valid(form)


class MailoutListView(ListView):
    model = Mailout
    form_class = MessageForm
    template_name = 'mailout/mailout.html'
    context_object_name = 'mailout'

    def get_context_data(self, **kwargs):
        context = super(MailoutListView, self).get_context_data(**kwargs)
        context['form'] = MailoutForm()
        return context


class MailoutDetailView(DetailView):
    model = Mailout
    template_name = 'mailout/mailout_view.html'
    context_object_name = 'mailout'


class MailoutUpdateView(UpdateView):
    model = Mailout
    form_class = MailoutForm
    template_name = 'mailout/mailout.html'
    success_url = reverse_lazy('mailout:mailout')

    def form_valid(self, form):
        mailout = form.save()

        if mailout.status == 'Завершена':
            mailout.sent_at = datetime.now()

        if mailout.status == 'Запущена':
            mailout.is_active = True

        mailout.save()

        return super().form_valid(form)


class MailoutDeleteView(DeleteView):
    model = Mailout
    success_url = reverse_lazy('mailout:mailout')
