# Generated by Django 4.0.1 on 2022-01-17 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_deck_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='answers',
            field=models.ManyToManyField(blank=True, null=True, related_name='decks', to='game.Answer', verbose_name='Ответы'),
        ),
        migrations.AlterField(
            model_name='deck',
            name='questions',
            field=models.ManyToManyField(blank=True, null=True, related_name='decks', to='game.Question', verbose_name='Вопросы'),
        ),
    ]
