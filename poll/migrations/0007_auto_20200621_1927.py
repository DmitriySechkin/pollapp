# Generated by Django 3.0.5 on 2020-06-21 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0006_auto_20200520_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='choice',
        ),
        migrations.AddField(
            model_name='survey',
            name='answer',
            field=models.TextField(default='', max_length=200),
            preserve_default=False,
        ),
    ]