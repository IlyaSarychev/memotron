from ..models import Profile


def register_new_user(form):
    '''Регистрация нового пользователя из формы'''
    
    if form.is_valid():
        cd = form.cleaned_data
        user = form.save(commit=False)
        user.set_password(cd['password1'])
        user.save()
        Profile.objects.create(user=user, name=cd['first_name'])
        return True
    else:
        return False