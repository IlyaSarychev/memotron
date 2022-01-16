from django import forms

from .models import Deck, Question, Answer
from account.services.utils.forms import process_form_fields


class CreateQuestionForm(forms.ModelForm):
    '''Форма создания вопроса пользователем'''

    class Meta:
        model = Question
        fields = ('text', 'is_published')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # изменение полей формы и их виджетов (например, добавление классов bootstrap)
        process_form_fields(self, checked=True)


class CreateAnswerForm(forms.ModelForm):
    '''Форма создания ответа пользователем'''

    class Meta:
        model = Answer
        fields = ['image', 'text', 'is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # изменение полей формы и их виджетов (например, добавление классов bootstrap)
        process_form_fields(self, checked=True, textarea_rows=1)


class CreateDeckForm(forms.ModelForm):
    '''Форма создания колоды'''

    class Meta:
        model = Deck
        fields = ['title', 'text', 'image', 'is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # изменение полей формы и их виджетов (например, добавление классов bootstrap)
        process_form_fields(self, checked=True, textarea_rows=1)
        
    