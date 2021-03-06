# Generated by Django 4.0.1 on 2022-01-24 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('game', '0010_game_membership_game_players_game_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='deck',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='game.deck', verbose_name='Колода'),
        ),
        migrations.AlterField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(related_name='game', through='game.Membership', to=settings.AUTH_USER_MODEL, verbose_name='Игроки'),
        ),
    ]
