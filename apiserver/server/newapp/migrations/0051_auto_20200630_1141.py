# Generated by Django 3.0.6 on 2020-06-30 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0050_auto_20200630_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duel',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=100),
        ),
    ]
