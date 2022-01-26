import os

from django.contrib.auth.models import User
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


def search_profiles(parameters):
    '''Поиск пользователей и их профилей. Необходимо передать параметры поиска (dict)'''

    filters = {}

    if 'name' in parameters:
        if 'id' in parameters: 
            filters['profile__extra_id__startswith'] = parameters.get('id')
            filters['first_name__iexact'] = parameters.get('name')
        else:
            filters['first_name__istartswith'] = parameters.get('name')
        

    users = User.objects.filter(**filters)[:10]

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