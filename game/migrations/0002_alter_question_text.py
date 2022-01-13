# Generated by Django 4.0.1 on 2022-01-11 17:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(20)], verbose_name='Текст вопроса'),
        ),
    ]