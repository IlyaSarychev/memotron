'''Сервисы для работы с ответами'''

from sorl.thumbnail import get_thumbnail

from game.models import Answer


def create_answer_by_form(request, answer_form):
    '''Создание ответа из формы и запроса'''

    answer = answer_form.save(commit=False)
    answer.user = request.user
    answer.save()

    return answer


def get_answer_thumbnail(answer):
    '''Получить sorl-thumbnail из объекта ответа'''

    return get_thumbnail(answer.image.path, '150x150', crop='center')


def delete_users_answer(answer_id, user):
    '''Удалить ответ пользователя. 
    Пользователя нужно передать, чтобы проверить, его ли это ответ.
    Возвращает количество удаленных записей'''

    return Answer.objects.get(id=answer_id, user=user).delete()[0]