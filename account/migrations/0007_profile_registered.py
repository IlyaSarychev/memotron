# Generated by Django 4.0.1 on 2022-01-24 08:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_following_profile_friends_following_friend1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='registered',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Зарегистрирован'),
            preserve_default=False,
        ),
    ]
