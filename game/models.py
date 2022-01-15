from django.db import models
from django.core.validators import MinLengthValidator


class Question(models.Model):
    '''Модель вопроса. Вопрос - часть игры memotron'''

    user = models.ForeignKey('auth.user', 
                             on_delete=models.CASCADE, 
                             related_name='questions')
    text = models.TextField('Текст вопроса',
                             validators=[MinLengthValidator(20)])
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
    created = models.DateTimeField('Дата создания', 
                                    auto_now_add=True)
    updated = models.DateTimeField('Дата обновления',
                                    auto_now=True,
                                    null=True)

    def __str__(self):
        return f'Ответ "{self.id}"'


class Deck(models.Model):
    '''Колода, включающая в себя карты с вопросами и карты с ответами.'''

    user = models.ForeignKey('auth.user', on_delete=models.CASCADE,
                            related_name='decks')
    title = models.CharField('Название колоды', max_length=250)
    text = models.TextField('Описание колоды', blank=True,
                            null=True)
    image = models.ImageField('Изображение', upload_to='deck/%Y/%m/%d',
                              blank=True,
                              null=True)
    questions = models.ManyToManyField(Question, related_name='decks')
    answers = models.ManyToManyField(Answer, related_name='decks')
    created = models.DateTimeField('Дата создания', 
                                    auto_now_add=True)
    updated = models.DateTimeField('Дата обновления',
                                    auto_now=True,
                                    null=True)