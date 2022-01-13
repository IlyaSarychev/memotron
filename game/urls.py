from django.urls import path
from . import views


app_name = 'game'

urlpatterns = [
    path('my-questions/', views.MyQuestionListView.as_view(), name='my_questions'),
    path('my-answers/', views.MyAnswersListView.as_view(), name='my_answers'),
    path('create-question-or-answer/', views.create_question_or_answer_view, 
                                       name='create_question_or_answer'),
    path('ajax-create-question/', views.ajax_create_question, name='ajax_create_question'),
    path('ajax-delete-question/<int:question_id>', views.ajax_delete_question, name='ajax_delete_question'),
]