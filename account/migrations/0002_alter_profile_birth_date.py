# Generated by Django 4.0.1 on 2022-01-07 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateTimeField(null=True, verbose_name='Дата рождения'),
        ),
    ]
