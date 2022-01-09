import os

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