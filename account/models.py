from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField('auth.user', on_delete=models.CASCADE,
                                related_name='profile')
    photo = models.ImageField(
                            verbose_name='Аватар профиля', 
                            upload_to='profile/%Y/%m/%d/',
                            null=True,
                            blank=True)
    birth_date = models.DateTimeField('Дата рождения', null=True, blank=True)
    friends = models.ManyToManyField('self', through='Following')
    registered = models.DateTimeField('Зарегистрирован', auto_now_add=True)
    extra_id = models.CharField('Идентификатор', max_length=4, db_index=True)

    def get_absolute_url(self):
        return reverse('account:account_profile', args=[self.id])


class Following(models.Model):
    '''Класс m2m для системы подписок пользователей друг на друга'''

    friend1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend2')
    date = models.DateTimeField('Начало дружбы', auto_now_add=True)