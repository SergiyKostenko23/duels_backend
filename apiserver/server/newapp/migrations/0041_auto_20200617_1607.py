# Generated by Django 3.0.6 on 2020-06-17 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0040_auto_20200615_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
