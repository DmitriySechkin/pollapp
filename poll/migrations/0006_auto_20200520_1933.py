# Generated by Django 3.0.5 on 2020-05-20 16:33

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0005_auto_20200516_2155'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='survey',
            managers=[
                ('custom_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]