# Generated by Django 3.0.6 on 2020-06-30 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0049_duel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duel',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
    ]