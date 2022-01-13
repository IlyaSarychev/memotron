import json

from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from account.services.utils.ajax import is_ajax
from .services.questions import create_question, delete_users_question
from .models import Question
from .forms import CreateQuestionForm


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


@login_required
def create_question_or_answer_view(request):
    '''Страница создания вопросов и ответов'''
    # Хотелось бы применить CreateView, но не придумал, как использовать 
    # CreateView вместе с несколькими моделями

    question_form = CreateQuestionForm()
    
    return render(request, 'question/create.html',
                  {'question_form': question_form})


@require_POST
@login_required
def ajax_create_question(request):
    '''Обработка AJAX-запроса на добавление вопроса'''

    if is_ajax(request):
        import json

        data = json.loads(request.body)

        try:
            q = create_question(data.get('text'), 
                                data.get('is_published'), 
                                request.user)
            return JsonResponse(
                {
                    'success': True,
                    'question': {
                        'id': q.id,
                        'text': q.text,
                        'is_published': q.is_published,
                        'created': q.created
                    }
                }
            )
        except ValidationError as err:
            return JsonResponse(
                {
                    'success': False,
                    'error': err.message_dict
                }
            )
    else:
        return HttpResponseForbidden()



@require_POST
@login_required
def ajax_delete_question(request, question_id):
    '''Обработка AJAX-запроса на удаление вопроса'''

    if not is_ajax(request):
        return HttpResponseForbidden()

    try:
        num = delete_users_question(question_id, request.user)
    except Exception as err:
        return JsonResponse({
            'success': False,
            'errors': err
        })

    return JsonResponse({'success': True, 'deleted_num': num})