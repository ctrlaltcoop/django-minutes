# Generated by Django 3.0.5 on 2020-04-26 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minutes.auth', '0002_token_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expires',
            field=models.DateTimeField(),
        ),
    ]
