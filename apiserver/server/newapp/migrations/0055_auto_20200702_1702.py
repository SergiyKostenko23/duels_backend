# Generated by Django 3.0.6 on 2020-07-02 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0054_auto_20200701_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='duels',
        ),
        migrations.AddField(
            model_name='result',
            name='duels',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='newapp.Duel'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='result',
            name='users',
        ),
        migrations.AddField(
            model_name='result',
            name='users',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
