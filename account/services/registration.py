from ..models import Profile


def register_new_user(form):
    '''Регистрация нового пользователя из формы'''
    
    if form.is_valid():
        cd = form.cleaned_data
        user = form.save(commit=False)
        user.set_password(cd['password1'])
        user.save()
        # добавление дополнительного id для отображения
        extra_id = ('0000' + str(user.id))[-4:]
        Profile.objects.create(user=user, name=cd['first_name'], extra_id=extra_id)
        return True
    else:
        return False