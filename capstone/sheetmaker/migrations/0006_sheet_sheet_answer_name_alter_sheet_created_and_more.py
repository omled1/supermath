# Generated by Django 4.1.4 on 2023-01-07 22:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheetmaker', '0005_alter_sheet_created_alter_sheet_modified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheet',
            name='sheet_answer_name',
            field=models.CharField(default='Answer Sheet', max_length=50),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 7, 22, 17, 28, 840299)),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 7, 22, 17, 28, 840465)),
        ),
    ]
