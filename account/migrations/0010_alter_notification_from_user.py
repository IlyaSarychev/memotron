# Generated by Django 4.0.1 on 2022-01-27 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0009_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outcome_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
