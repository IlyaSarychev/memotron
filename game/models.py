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

    class Meta:
        ordering = ('-created',)

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

    class Meta:
        ordering = ('-created',)

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
    questions = models.ManyToManyField(Question, related_name='decks',
                                        verbose_name='Вопросы',
                                        blank=True)
    answers = models.ManyToManyField(Answer, related_name='decks',
                                        verbose_name='Ответы',
                                        blank=True)
    is_published = models.BooleanField('Ответ опубликован?', 
                                        default=False)
    created = models.DateTimeField('Дата создания', 
                                    auto_now_add=True)
    updated = models.DateTimeField('Дата обновления',
                                    auto_now=True,
                                    null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_question_ids(self, template=True):
        '''Получить список id вопросов конкретной колоды.
        Если template=True, то список вернется в отформатированном для шаблона виде'''
        if template:
            return ','.join([str(q['id']) for q in self.questions.values('id')])

    def get_answer_ids(self, template=True):
        '''Получить список id ответов конкретной колоды.
        Если template=True, то список вернется в отформатированном для шаблона виде'''
        if template:
            return ','.join([str(a['id']) for a in self.answers.values('id')])



class Game(models.Model):
    '''Модель игры. Содержит некоторые данные об игре. Основные данные хранятся в Redis во время игры.'''

    user = models.ForeignKey('auth.user', on_delete=models.CASCADE,
                            related_name='games')
    players = models.ManyToManyField('auth.user', 
                                     related_name='game', 
                                     through='Membership', 
                                     verbose_name='Игроки')
    is_active = models.BooleanField('Игра запущена?', db_index=True,
                                    default=False)
    deck = models.OneToOneField(Deck, 
                                on_delete=models.CASCADE,
                                related_name='game',
                                verbose_name='Колода')
    created = models.DateTimeField('Дата создания игры', auto_now_add=True)


class Membership(models.Model):
    '''Модель для связи many-to-many User и Game, чтобы хранить дополнительные поля'''

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='memberships')
    answers = models.IntegerField('Количество ответов всего', default=0)
    wins = models.IntegerField('Количество побед', default=0)