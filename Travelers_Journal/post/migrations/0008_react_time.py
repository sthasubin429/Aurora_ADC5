# Generated by Django 3.0.1 on 2020-02-07 18:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='react',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 8, 0, 24, 46, 685070)),
        ),
    ]
