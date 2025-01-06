import secrets
import os

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from dotenv import load_dotenv

from users.forms import UserRegisterForm
from users.models import User

load_dotenv(override=True)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(5)
        user.token = token
        user.save()
        url = f'http://{self.request.get_host()}/users/email_confirm/{token}/'

        send_mail(
            "Подтверждение адреса электронной почты",
            f"Подтвердите регистацию на сайте Skystore. Перейдите по ссылке: {url} .",
            os.getenv("EMAIL_HOST_USER"),
            [f"{user.email}"],
            fail_silently=False,
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
