from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .forms import AccountLoginForm, AccountRegistrationForm
from .models import Profile, Notification
from .services.registration import register_new_user
from .services import profile_serv
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
            return redirect('account:self_account_profile')
        else:
            return render(request, 'account/registration.html', {'form': form})
    else:
        # Вернуть шаблон страницы
        form = AccountRegistrationForm()
    return render(request, 'account/registration.html', {'form': form})


@login_required
def account_profile(request, profile_id=None):
    '''Страница профиля'''
    if not profile_id:
        profile = get_object_or_404(Profile, id=request.user.profile.id)
        return render(request, 'account/profile/detail.html',
                            {'profile': profile})
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'account/profile/detail.html',
                            {'profile': profile})


@require_POST
def profile_change_photo(request):
    '''Изменение фото профиля из ajax-запроса'''
    if is_ajax(request):
        success, profile = profile_serv.change_profile_photo(request)
        if success:
            return JsonResponse({'url': profile.photo.url})
        else:
            return JsonResponse({'error': 'Что-то пошло не так'})
    else:
        return HttpResponseForbidden()


@require_GET
@login_required
def ajax_search_profiles(request):
    '''Поиск пользователей через AJAX'''
    
    if not is_ajax(request):
        return HttpResponseForbidden()

    data = profile_serv.search_profiles(request.user, request.GET)

    return JsonResponse(data)



@require_POST
@login_required
def ajax_invite_friends(request):
    '''Приглашение в друзья через AJAX'''

    if not is_ajax(request):
        return HttpResponseForbidden()

    user_ids = [int(id) for id in request.POST.get('user_ids').split(',')]
    profile_serv.invite_friends(request.user, user_ids)

    return JsonResponse({
        'success': True
    })


class NotificationListView(ListView):
    '''Список уведомлений'''

    context_object_name = 'notifications'
    template_name = 'notifictation/list.html'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)