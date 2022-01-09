from django.urls import path
from . import views


app_name = 'game'

urlpatterns = [
    path('my-questions/', views.MyQuestionListView.as_view(), name='my_questions'),
]