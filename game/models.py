from django.db import models


class Question(models.Model):
    '''Модель вопроса. Вопрос - часть игры memotron'''

    user = models.ForeignKey('auth.user', 
                             on_delete=models.CASCADE, 
                             related_name='questions')
    text = models.TextField('Текст вопроса')
    created = models.DateTimeField('Дата создания', 
                                    auto_now_add=True)
    updated = models.DateTimeField('Дата обновления',
                                    auto_now=True,
                                    null=True)
    is_published = models.BooleanField('Вопрос опубликован?', 
                                        default=False)

    def __str__(self):
        return f'Вопрос: "{self.text[:20]}"'


class Answer(models.Model):
    '''Модель ответа. Ответ - часть игры memotron'''

    user = models.ForeignKey('auth.user', 
                             on_delete=models.CASCADE, 
                             related_name='answers')
    image = models.ImageField('Изображение', upload_to='answer/%Y/%m/%d/')
    text = models.TextField('Текст ответа', blank=True, null=True)
    is_published = models.BooleanField('Ответ опубликован?', 
                                        default=False)

    def __str__(self):
        return f'Ответ "{self.id}"'