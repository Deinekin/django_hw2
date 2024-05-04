import secrets
import random
from django.shortcuts import render

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UpdatePasswordForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def update_password(request):
    return render(request, 'users/update_password.html')


def generate_and_send_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.get(email=email)
        new_password = make_password(''.join(str(random.randint(0, 9)) for _ in range(16)))
        user.set_password(new_password)

        send_mail(
            subject="Новый пароль",
            message=f"Новый пароль для входа: {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        user.save()

    return render(request, 'users/update_password.html')


class UpdatePassword(FormView):
    form_class = UpdatePasswordForm
    template_name = 'users/update_password.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            new_password = ''.join(str(random.randint(0, 9)) for _ in range(16))
            user.password = make_password(new_password)
            send_mail(
                subject='Вы сменили пароль',
                message=f'Ваш новый пароль {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            user.save()

        return super().form_valid(form)
