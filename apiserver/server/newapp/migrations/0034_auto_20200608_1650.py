# Generated by Django 3.0.6 on 2020-06-08 15:50

from django.db import migrations, models
import newapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0033_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdf',
            name='pdf',
            field=models.FileField(upload_to='C:\\Users\\sergy.kostenko\\Desktop\\apiserver\\server\\media\\pdf', validators=[newapp.validators.valida_pdf]),
        ),
    ]
