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
    path('ajax-update-question/<int:question_id>', views.ajax_update_question, name='ajax_update_question'),
    path('ajax-create-answer/', views.ajax_create_answer, name='ajax_create_answer'),
    path('ajax-delete-answer/<int:answer_id>', views.ajax_delete_answer, name='ajax_delete_answer'),

    # колода
    path('create-deck/', views.create_deck_view, name='create_deck'),
    path('my-decks/', views.DeckListView.as_view(), name='my_decks'),
    path('ajax-create-deck/', views.ajax_create_deck, name='ajax_create_deck'),
    path('ajax-delete-deck/<int:deck_id>', views.ajax_delete_deck, name='ajax_delete_deck'),
]