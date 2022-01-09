from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Question


class MyQuestionListView(ListView):
    '''Список вопросов пользователя'''
    model = Question
    context_object_name = 'questions_list'
    template_name = 'question/list.html'

    class Meta:
        ordering = ('-created',)

    def get_queryset(self):
        '''Взять только вопросы пользователя'''
        return Question.objects.filter(user__id=self.request.user.id)

    # Доступ к view только атворизованным пользователям
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)