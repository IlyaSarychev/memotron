from django import forms
from .models import Question, Answer
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