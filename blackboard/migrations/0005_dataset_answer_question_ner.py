# Generated by Django 2.2.7 on 2020-01-29 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blackboard', '0004_auto_20191207_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset_answer',
            name='question_ner',
            field=models.CharField(default='', max_length=300),
        ),
    ]
