from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


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


class AccountRegistrationForm(forms.ModelForm):
    '''Форма регистрации пользователя'''

    # Поля
    password1 = forms.CharField(label='Пароль', 
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', 
                                widget=forms.PasswordInput())

    error_css_class = 'is-invalid'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def is_valid(self):
         result = super().is_valid()
         # loop on *all* fields if key '__all__' found else only on errors:
         for x in (self.fields if '__all__' in self.errors else self.errors):
             attrs = self.fields[x].widget.attrs
             attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
         return result

    # Проверить, существует ли пользователь с таким именем
    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise ValidationError('Такое имя уже существует')

        return self.cleaned_data['username']