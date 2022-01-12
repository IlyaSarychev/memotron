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