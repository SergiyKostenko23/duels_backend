# Generated by Django 3.0.6 on 2020-06-08 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0028_auto_20200608_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='C:\\Users\\sergy.kostenko\\Desktop\\apiserver\\server\\media\\img\\placeholder.jpg', upload_to='C:\\Users\\sergy.kostenko\\Desktop\\apiserver\\server\\media\\img'),
        ),
    ]
