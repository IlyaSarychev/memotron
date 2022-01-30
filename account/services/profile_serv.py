import imp
import os

from django.urls import reverse
from django.contrib.auth.models import User
from account.models import Notification
from ..models import Profile
from ..forms import UploadFileForm


def change_profile_photo(request):
    '''Меняет фото профиля пользователя и удаляет старое. 
    В случае успеха возвращает True и модель профиля'''
    form = UploadFileForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        profile = Profile.objects.get(id=request.user.profile.id)

        # Удалить текущее фото
        if profile.photo:
            os.remove(profile.photo.path)

        profile.photo = request.FILES.get('file')
        profile.save()
        
        return True, profile
    else:
        return False


def search_profiles(user, parameters):
    '''Поиск пользователей и их профилей. Необходимо передать параметры поиска (dict)'''

    filters = {}
    if 'name' in parameters:
        if 'id' in parameters: 
            filters['profile__extra_id__startswith'] = parameters.get('id')
            filters['first_name__iexact'] = parameters.get('name')
        else:
            filters['first_name__istartswith'] = parameters.get('name')

    users = User.objects.filter(**filters).exclude(id=user.id)[:10]
    data = {
        'users': []
    }

    for user in users:
        data['users'].append({
            'id': user.id,
            'username': user.first_name,
            'extra_id': user.profile.extra_id,
            'profile_url': user.profile.get_absolute_url()
        })

    return data


def invite_friends(from_user, to_users):
    '''Пригласить друзей'''
    
    for user_id in to_users:
        typeof = 'friend_adding'
        title = f'Пользователь <a href="{from_user.profile.get_absolute_url()}">{from_user.first_name}#{from_user.profile.extra_id}</a> хочет добавить вас в друзья'
        Notification.objects.get_or_create(from_user=from_user,
                                            user=User.objects.get(id=user_id),
                                            typeof=typeof,
                                            title=title)


def set_notifications_viewed(ids):
    '''Сделать уведомления просмотренными по их id'''

    return Notification.objects.filter(id__in=ids).update(is_viewed=True)