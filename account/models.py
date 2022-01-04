from django.db import models


class Profile(models.Model):
    user = models.OneToOneField('auth.user', on_delete=models.CASCADE,
                                related_name='profile')
    photo = models.ImageField(verbose_name='Аватар профиля', upload_to='media/%Y/%m/%d/')
    name = models.CharField('Имя', max_length=100)
    birth_date = models.DateTimeField('Дата рождения')

