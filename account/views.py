from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .forms import AccountLoginForm, AccountRegistrationForm
from .models import Profile
from .services.registration import register_new_user
from .services.profile import change_profile_photo
from .services.utils.ajax import is_ajax


class LoginView(auth_views.LoginView):
    '''Страница входа'''
    authentication_form = AccountLoginForm


def account_register_new_user(request):
    '''Страница регистрации'''
    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        success = register_new_user(form)
        if success:
            return redirect('account:account_profile')
        else:
            return render(request, 'account/registration.html', {'form': form})
    else:
        # Вернуть шаблон страницы
        form = AccountRegistrationForm()
    return render(request, 'account/registration.html', {'form': form})


@login_required
def account_profile(request, profile_id):
    '''Страница профиля'''
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'account/profile/detail.html',
                            {'profile': profile})


@require_POST
def profile_change_photo(request):
    '''Изменение фото профиля из ajax-запроса'''
    if is_ajax(request):
        success, profile = change_profile_photo(request)
        if success:
            return JsonResponse({'url': profile.photo.url})
        else:
            return JsonResponse({'error': 'Что-то пошло не так'})
    else:
        return HttpResponseForbidden()