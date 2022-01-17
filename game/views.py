from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from account.services.utils.ajax import is_ajax
from .services import questions, answers, deck_service
from .models import Answer, Deck, Question
from .forms import CreateQuestionForm, CreateAnswerForm, CreateDeckForm


class MyQuestionListView(ListView):
    '''Список вопросов пользователя'''
    model = Question
    context_object_name = 'questions_list'
    template_name = 'question/list.html'

    def get_queryset(self):
        '''Взять только вопросы пользователя'''
        return Question.objects.filter(user__id=self.request.user.id)

    # Доступ к view только атворизованным пользователям
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class MyAnswersListView(ListView):
    '''Список ответов пользователя'''
    model = Answer
    context_object_name = 'answers_list'
    template_name = 'answer/list.html'

    def get_queryset(self):
        '''Взять только ответы пользователя'''
        return Answer.objects.filter(user__id=self.request.user.id)

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
    answer_form = CreateAnswerForm()
    
    return render(request, 'create.html',
                  {'question_form': question_form,
                   'answer_form': answer_form})


@require_POST
@login_required
def ajax_create_question(request):
    '''Обработка AJAX-запроса на добавление вопроса'''

    if is_ajax(request):
        import json
        data = json.loads(request.body)
        try:
            q = questions.create_question(data.get('text'), 
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
        num = questions.delete_users_question(question_id, request.user)
    except Exception as err:
        return JsonResponse({
            'success': False,
            'errors': err
        })
    else:
        return JsonResponse({'success': True, 'deleted_num': num})


@require_POST
@login_required
def ajax_update_question(request, question_id):
    '''Обработка AJAX-запроса на изменение вопроса'''

    if not is_ajax(request):
        return HttpResponseForbidden()

    try:
        import json

        data = json.loads(request.body)
        questions.update_question(id=question_id, **data)
    except Exception as err:
        return JsonResponse({
            'success': False,
            'errors': err
        })
    else:
        return JsonResponse({'success': True})


@require_POST
@login_required
def ajax_create_answer(request):
    '''Обработка AJAX-запроса на добавление ответа пользователем'''

    if not is_ajax(request):
        return HttpResponseForbidden()

    form = CreateAnswerForm(request.POST, request.FILES)
    if form.is_valid():
        answer = answers.create_answer_by_form(request, form)
        answer_thumbnail = answers.get_answer_thumbnail(answer)
        
        return JsonResponse({
            'success': True,
            'answer': {
                'text': answer.text,
                'image_url': answer.image.url,
                'is_published': answer.is_published,
                'thumbnail_url': answer_thumbnail.url
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })
        

@require_POST
@login_required
def ajax_delete_answer(request, answer_id):
    '''Обработка AJAX-запроса на удаление ответа'''

    if not is_ajax(request):
        return HttpResponseForbidden()
    try:
        num = answers.delete_users_answer(answer_id, request.user)
    except Exception as err:
        return JsonResponse({
            'success': False,
            'errors': err
        })
    else:
        return JsonResponse({'success': True, 'deleted_num': num})


# Колоды
class DeckListView(ListView):
    '''Страница всех колод пользователя'''

    model = Deck
    context_object_name = 'deck_list'
    template_name = 'deck/list.html'

    def get_queryset(self):
        '''Взять только вопросы пользователя'''
        return Deck.objects.filter(user__id=self.request.user.id)

    # Доступ к view только атворизованным пользователям
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@login_required
def create_deck_view(request):
    '''Страница создания колоды'''

    user = request.user
    form = CreateDeckForm()
    questions = user.questions.all()
    answers = user.answers.all()
    return render(request, 'deck/create.html', 
                    {
                        'form': form,
                        'questions': questions,
                        'answers': answers
                    })


@login_required
@require_POST
def ajax_create_deck(request):
    '''Обработка AJAX-запроса на создание колоды'''

    if not is_ajax(request):
        return HttpResponseForbidden()

    success, form, deck = deck_service.create_deck_from_request_with_form(request)

    if success:
        return JsonResponse({
            'success': True,
            'deck': {
                'title': deck.title,
                'text': deck.text,
                'image': deck.image.url if deck.image else None,
                'is_published': deck.is_published,
                'created': deck.created
            },
            'errors': dict(form.errors)
        })
    else:
        return JsonResponse({
            'success': False,
            'deck': None,
            'errors': dict(form.errors)
        })