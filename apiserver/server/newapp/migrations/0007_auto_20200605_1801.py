# Generated by Django 3.0.6 on 2020-06-05 17:01

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0006_auto_20200605_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='media/videos/'), upload_to='../videos/'),
        ),
    ]
