# Generated by Django 3.0.6 on 2020-06-24 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0044_auto_20200624_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]