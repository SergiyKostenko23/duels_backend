# Generated by Django 3.0.6 on 2020-06-08 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0029_auto_20200608_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='tipo_ficheiro',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
