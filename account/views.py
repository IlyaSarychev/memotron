from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import AccountLoginForm, AccountRegistrationForm
from .models import Profile


@login_required
def account_profile(request, profile_id):
    '''Вью для страницы профиля'''
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'account/profile/detail.html',
                            {'profile': profile})


class LoginView(auth_views.LoginView):
    '''Вью для страницы входа'''
    authentication_form = AccountLoginForm


def account_register_new_user(request):
    if request.method == 'POST':
        # Регистрация пользователя
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)

            user.set_password(cd['password1'])
            user.save()
            Profile.objects.create(user=user, name=cd['first_name'])
            
            return redirect('account:account_profile')
        else:
            return render(request, 'account/registration.html', {'form': form})
    else:
        # Вернуть шаблон страницы
        form = AccountRegistrationForm()
    return render(request, 'account/registration.html', {'form': form})