from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class AccountLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': ''
            }
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': ''
            }
        )
    )