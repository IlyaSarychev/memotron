'''Сервисы для работы с вопросами'''

from django.core.exceptions import ValidationError
from ..models import Question


def create_question(text, is_published, user):
    '''Создать вопрос'''

    try:
        question = Question(text=text, 
                            is_published=is_published,
                            user=user)
        question.full_clean()
        question.save()
        
    except ValidationError as err:
        raise err

    return question


def delete_users_question(id, user):
    '''Удалить вопрос пользователя. 
    Пользователя нужно передать, чтобы проверить, его ли это вопрос.
    Возвращает количество удаленных записей'''

    return Question.objects.get(id=id, user=user).delete()[0]


def update_question(id, **updates):
    '''Изменить вопрос'''

    Question.objects.filter(id=id).update(**updates)