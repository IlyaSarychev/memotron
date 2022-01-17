'''Сервисы для работы с колодами'''

from ..forms import CreateDeckForm
from ..models import Deck


def create_deck_from_request_with_form(request):
    '''Создать колоду из запроса с помощью формы.
    Возвращает True/False в зависимости от form.is_valid(),
    объект CreateDeckForm, объект Deck/None в зависимости от form.is_valid()'''

    form = CreateDeckForm(request.POST, request.FILES)

    if form.is_valid():
        deck = form.save(commit=False)
        deck.user = request.user
        # нужно сохранить объект в базе данных прежде, чем добавлять many-to-many значения
        # это нужно, чтобы у объекта в бд появился id
        deck.save()
        if len(request.POST.get('questions')) > 0:
            deck.questions.add(*[int(i) for i in request.POST.get('questions').split(',')])
        if len(request.POST.get('answers')) > 0:
            deck.answers.add(*[int(i) for i in request.POST.get('answers').split(',')])
        deck.save()
        
        return True, form, deck
    else:
        return False, form, None


def delete_deck(deck_id, user):
    '''Удалить колоду по id. Необходимо передать user, 
    чтобы пользователь удалял только свои колоды'''
    
    return Deck.objects.filter(id=deck_id, user__id=user.id).delete()[0]