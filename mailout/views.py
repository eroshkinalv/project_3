import os
from datetime import datetime

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from dotenv import load_dotenv
from django.core.mail import send_mail

from .forms import ClientsForm, MessageForm, MailoutForm, AttemptForm, ManagerForm
from .models import Home, Clients, Message, Mailout, Attempt
from .services import get_clients_from_cache

load_dotenv(override=True)


class HomeTemplateView(TemplateView):
    template_name = 'mailout/home.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:

            total_emails = int(Attempt.objects.filter(owner=user).count())
            mailing_success = int(Attempt.objects.filter(owner=user, status='Успешно').count())
            percent_success = round((mailing_success * 100) / total_emails)
            mailing_fail = Attempt.objects.filter(owner=user, status='Не успешно').count()
            percent_fail = round((mailing_fail * 100) / total_emails)

            data = {'mailing_active': Mailout.objects.filter(is_active=True).count(),
                    'mailing': Mailout.objects.all().count(),
                    'clients': Clients.objects.distinct('email').count(),
                    'total_emails': Mailout.objects.filter(owner=user).count(),
                    'mailing_success': Attempt.objects.filter(owner=user, status='Успешно').count(),
                    'mailing_fail': Attempt.objects.filter(owner=user, status='Не успешно').count(),
                    'percent_success': percent_success,
                    'percent_fail': percent_fail
                    }

            context.update(data)
            return context

        data = {'mailing_active': Mailout.objects.filter(is_active=True).count(),
                'mailing': Mailout.objects.all().count(),
                'clients': Clients.objects.distinct('email').count(),
                }

        context.update(data)
        return context


class HomeCreateView(CreateView):
    model = Home
    fields = ('total_users', 'total_mailout', 'total_active')
    template_name = 'mailout/home.html'
    success_url = reverse_lazy('mailout:home')


class ClientsCreateView(LoginRequiredMixin, CreateView):
    model = Clients
    form_class = ClientsForm
    template_name = 'mailout/clients_create.html'
    success_url = reverse_lazy('mailout:clients')

    def form_valid(self, form):
        clients = form.save()
        user = self.request.user
        clients.owner = user
        clients.save()
        return super().form_valid(form)


class ClientsListView(LoginRequiredMixin, ListView):
    model = Clients
    template_name = 'mailout/clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        queryset = get_clients_from_cache()
        return queryset

    def get_context_data(self, **kwargs):

        user = self.request.user
        context = super(ClientsListView, self).get_context_data(**kwargs)
        context['form'] = ClientsForm()

        if user.has_perm("product.can_view_client_info"):
            return context

        context['clients'] = Clients.objects.filter(owner=user)
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ClientsDetailView(LoginRequiredMixin, DetailView):
    model = Clients
    template_name = 'mailout/client_view.html'
    context_object_name = 'client'


class ClientsUpdateView(LoginRequiredMixin, UpdateView):
    model = Clients
    form_class = ClientsForm
    template_name = 'mailout/clients.html'
    success_url = reverse_lazy('mailout:clients')


class ClientsDeleteView(LoginRequiredMixin, DeleteView):
    model = Clients
    success_url = reverse_lazy('mailout:clients')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailout/message_create.html'
    success_url = reverse_lazy('mailout:message')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailout/messages.html'
    context_object_name = 'messages'

    def get_context_data(self, **kwargs):

        user = self.request.user
        context = super(MessageListView, self).get_context_data(**kwargs)
        context['form'] = MessageForm()

        if user.has_perm("product.can_view_messages"):
            return context

        context['messages'] = Message.objects.filter(owner=user)
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailout/message_view.html'
    context_object_name = 'message'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailout/messages.html'
    success_url = reverse_lazy('mailout:message')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailout:message')


class MailoutCreateView(LoginRequiredMixin, CreateView):
    model = Mailout
    form_class = MailoutForm
    template_name = 'mailout/mailout_create.html'
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


class MailoutListView(LoginRequiredMixin, ListView):
    model = Mailout
    form_class = MessageForm
    template_name = 'mailout/mailout.html'
    context_object_name = 'mailout'

    def get_context_data(self, **kwargs):

        user = self.request.user
        context = super(MailoutListView, self).get_context_data(**kwargs)
        context['form'] = MailoutForm()

        if user.has_perm("product.can_view_mailout"):
            return context

        context['mailout'] = Mailout.objects.filter(owner=user)
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailoutDetailView(LoginRequiredMixin, DetailView):
    model = Mailout
    template_name = 'mailout/mailout_view.html'
    context_object_name = 'mailout'


class MailoutUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailout
    form_class = MailoutForm
    template_name = 'mailout/mailout.html'
    success_url = reverse_lazy('mailout:mailout')

    def get_form_class(self):
        user = self.request.user

        if user == self.object.owner:
            return MailoutForm

        if user.has_perm("product.can_unpublish_products"):
            return ManagerForm

        raise PermissionDenied

    def form_valid(self, form):
        mailout = form.save()

        if mailout.status == 'Завершена':
            mailout.sent_at = datetime.now()

        if mailout.status == 'Запущена':
            mailout.is_active = True

        mailout.save()

        return super().form_valid(form)


class MailoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailout
    success_url = reverse_lazy('mailout:mailout')


class AttemptCreateView(LoginRequiredMixin, CreateView):
    model = Attempt
    form_class = AttemptForm
    template_name = 'mailout/attempt.html'
    success_url = reverse_lazy('mailout:attempt')

    def form_valid(self, form):

        clients = form.save()
        user = self.request.user
        clients.owner = user
        clients.save()

        attempt = form.save()

        try:

            send_mail(
                f"{attempt.mailout.message.subject}",
                f"{attempt.mailout.message.message}",
                os.getenv("EMAIL_HOST_USER"),
                [client.email for client in attempt.mailout.clients.all()],
                fail_silently=False,
            )

        except Exception as e:
            attempt.server_message = e
            attempt.status = 'Не успешно'

        else:
            attempt.server_message = 'Сообщение отправлено'
            attempt.status = 'Успешно'

        return super().form_valid(form)


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    form_class = AttemptForm
    template_name = 'mailout/attempt.html'
    context_object_name = 'attempts'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['form'] = AttemptForm()

        if user.is_authenticated:

            total_emails = int(Attempt.objects.filter(owner=user).count())
            mailing_success = int(Attempt.objects.filter(owner=user, status='Успешно').count())
            percent_success = round((mailing_success * 100) / total_emails)
            mailing_fail = Attempt.objects.filter(owner=user, status='Не успешно').count()
            percent_fail = round((mailing_fail * 100) / total_emails)

            data = {'total_emails': Attempt.objects.filter(owner=user).count(),
                    'mailing_success': Attempt.objects.filter(owner=user, status='Успешно').count(),
                    'mailing_fail': Attempt.objects.filter(owner=user, status='Не успешно').count(),
                    'percent_success': percent_success,
                    'percent_fail': percent_fail
                    }

            context.update(data)
            return context

        data = {'mailing_active': Mailout.objects.filter(is_active=True).count(),
                'mailing': Mailout.objects.all().count(),
                'clients': Clients.objects.distinct('email').count(),
                }

        context.update(data)
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class AttemptDetailView(LoginRequiredMixin, DetailView):
    model = Attempt
    template_name = 'mailout/attempt_view.html'
    context_object_name = 'attempt'


class AttemptUpdateView(LoginRequiredMixin, UpdateView):
    model = Attempt
    form_class = AttemptForm
    template_name = 'mailout/attempt.html'
    success_url = reverse_lazy('mailout:attempt')


class AttemptDeleteView(LoginRequiredMixin, DeleteView):
    model = Attempt
    success_url = reverse_lazy('mailout:attempt')


class StatisticsTemplateView(LoginRequiredMixin, TemplateView):
    model = Mailout
    template_name = 'mailout/statistics.html'
    success_url = reverse_lazy('mailout:statistics')

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        total_emails = int(Attempt.objects.filter(owner=user).count())
        mailing_success = int(Attempt.objects.filter(owner=user, status='Успешно').count())
        percent_success = round((mailing_success * 100) / total_emails)
        mailing_fail = Attempt.objects.filter(owner=user, status='Не успешно').count()
        percent_fail = round((mailing_fail * 100) / total_emails)

        total_mailing = Mailout.objects.filter(owner=user).count()
        active_mailing = Mailout.objects.filter(owner=user, is_active=True).count()
        completed_mailing = Mailout.objects.filter(owner=user, status='Завершена').count()
        percent_active = round((active_mailing * 100) / total_mailing)
        percent_completed = round((completed_mailing * 100) / total_mailing)

        total_messages_by_user = Message.objects.filter(owner=user).count()
        total_clients_by_user = Clients.objects.filter(owner=user).count()
        all_messages = Message.objects.count()
        all_clients = Clients.objects.count()
        percent_messages = round((total_messages_by_user * 100) / all_messages)
        percent_clients = round((total_clients_by_user * 100) / all_clients)

        data = {'total_messages': Message.objects.filter(owner=user).count(),
                'percent_messages': percent_messages,
                'total_clients': Clients.objects.filter(owner=user).count(),
                'percent_clients': percent_clients,

                'total_mailing': Mailout.objects.filter(owner=user).count(),
                'active_mailing': Mailout.objects.filter(owner=user, is_active=True).count(),
                'completed_mailing': Mailout.objects.filter(owner=user, status='Завершена').count(),
                'percent_active': percent_active,
                'percent_completed': percent_completed,

                'total_emails': Attempt.objects.filter(owner=user).count(),
                'mailing_success': Attempt.objects.filter(owner=user, status='Успешно').count(),
                'mailing_fail': Attempt.objects.filter(owner=user, status='Не успешно').count(),
                'percent_success': percent_success,
                'percent_fail': percent_fail
                }

        context.update(data)
        return context
