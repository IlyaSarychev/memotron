from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import forms, views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .forms import AccountLoginForm, AccountRegistrationForm, UploadFileForm
from .models import Profile


class LoginView(auth_views.LoginView):
    '''Вью для страницы входа'''
    authentication_form = AccountLoginForm


def account_register_new_user(request):
    '''Вью для страницы регистрации'''
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


@login_required
def account_profile(request, profile_id):
    '''Вью для страницы профиля'''
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'account/profile/detail.html',
                            {'profile': profile})


@require_POST
def profile_change_photo(request):
    '''Вью для изменения фото профиля'''
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = UploadFileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            profile = Profile.objects.get(id=request.user.profile.id)
            profile.photo = request.FILES.get('file')
            profile.save()
            return HttpResponse('Валидно')
        else:
            print(form.errors)
            return HttpResponse('Не валидно')
    else:
        return HttpResponseForbidden()