# Generated by Django 3.0.5 on 2020-05-16 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_question_type_question'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survey',
            options={'ordering': ['-pub_date']},
        ),
    ]
