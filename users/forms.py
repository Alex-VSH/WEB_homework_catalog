from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'user_phone', 'user_avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class ChangePassForm(forms.Form):
    user_email = forms.CharField(help_text="Введите почту для которой нужно восстановить пароль")
