# Generated by Django 3.0.1 on 2020-01-25 04:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200125_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 25, 10, 27, 45, 501985)),
        ),
    ]
