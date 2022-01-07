from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import AccountLoginForm, AccountRegistrationForm


@login_required
def account_profile(request):
    '''Вью для страницы профиля'''
    return render(request, 'account/profile/detail.html')


class LoginView(auth_views.LoginView):
    '''Вью для страницы входа'''
    authentication_form = AccountLoginForm


def account_register_new_user(request):
    if request.method == 'POST':
        # Регистрация пользователя
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
        else:
            return render(request, 'account/registration.html', {'form': form})
    else:
        # Вернуть шаблон страницы
        form = AccountRegistrationForm()
    return render(request, 'account/registration.html', {'form': form})