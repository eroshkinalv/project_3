import secrets
import os
import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, ListView
from dotenv import load_dotenv

from users.forms import UserRegisterForm, UserUpdateForm, PasswordUpdateForm, ManagerForm
from users.models import User

load_dotenv(override=True)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:login')
    context_object_name = 'users'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(5)
        user.token = token
        user.save()
        url = f'http://{self.request.get_host()}/users/email_confirm/{token}/'

        send_mail(
            "Подтверждение адреса электронной почты",
            f"Подтвердите регистацию на сайте Mailout. Перейдите по ссылке: {url} .",
            os.getenv("EMAIL_HOST_USER"),
            [f"{user.email}"],
            fail_silently=False,
        )

        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update_form.html'
    success_url = reverse_lazy('mailout:home')


class UserListView(ListView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):

        user = self.request.user
        context = super(UserListView, self).get_context_data(**kwargs)

        if user.has_perm("managers"):
            context["status"] = "Менеджер"
            return context

        context["status"] = "Пользователь"
        return context


class UserDetailView(DetailView):
    model = User
    template_name = 'users/personal_account.html'
    context_object_name = 'user'


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class PasswordTemplateView(TemplateView):

    form_class = PasswordUpdateForm
    template_name = 'users/password_form.html'
    success_url = reverse_lazy('users:login')

    def post(self, request):

        if request.method == 'POST':
            email = request.POST.get('email')
            user = User.objects.filter(email=email).first()
            if user:

                password = str(random.randint(10000000, 99999999))
                user.set_password(password)
                user.save()

                send_mail(
                    "Смена пароля",
                    f"Ваш новый пароль: {password} .",
                    os.getenv("EMAIL_HOST_USER"),
                    [f"{email}"],
                    fail_silently=False,
                )

        return render(request, 'login.html')

    def get_context_data(self, **kwargs):

        context = super(PasswordTemplateView, self).get_context_data(**kwargs)
        context['form'] = PasswordUpdateForm()

        return context


class ManagerUpdateView(UpdateView):
    model = User
    form_class = ManagerForm
    template_name = 'users/user_update_form.html'
    success_url = reverse_lazy('mailout:home')


class ManagerDetailView(DetailView):
    model = User
    template_name = 'users/manager_view.html'
    context_object_name = 'user'
