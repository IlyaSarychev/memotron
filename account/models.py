from django.db import models


class Profile(models.Model):
    user = models.OneToOneField('auth.user', on_delete=models.CASCADE,
                                related_name='profile')
    photo = models.ImageField(
                            verbose_name='Аватар профиля', 
                            upload_to='profile/%Y/%m/%d/',
                            null=True,
                            blank=True)
    birth_date = models.DateTimeField('Дата рождения', null=True, blank=True)

