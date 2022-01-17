from django.contrib import admin
from .models import Question, Answer, Deck


admin.site.register(Question)
admin.site.register(Answer)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    '''Отображение колоды в админке'''

    list_display = ('id', 'title', 'is_published', 'created', 'updated')
    list_display_links = ('id', 'title')