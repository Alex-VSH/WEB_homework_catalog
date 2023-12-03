from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template import context
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, ChangePassForm
from users.models import User
from django.utils.crypto import get_random_string


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        token = get_random_string(length=32)
        user = form.save(commit=False)
        user.token = token
        user.save()

        verification_url = f'http://127.0.0.1:8000{reverse_lazy("users:verification", args=[token])}'
        send_mail(subject='Ваша ссылка для подтверждения регистрации', message=verification_url, from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[user.email], fail_silently=False)
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def verification_view(requests, token):
    user = User.objects.filter(token=token).first()
    if user:
        user.is_active = True
        user.token = None
        user.save()
    return redirect('users:login')



def restore_user(request):
    form = ChangePassForm()
    if request.method == 'POST':
        email = request.POST.get('user_email')
        user = User.objects.get(email=email)
        new_password = get_random_string(length=14)
        send_mail(
            subject='Ваш новый пароль', message=new_password,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email], fail_silently=False
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse('users:login'))
    else:
        return render(request, 'users/password_reset_email.html', {"form": form})



