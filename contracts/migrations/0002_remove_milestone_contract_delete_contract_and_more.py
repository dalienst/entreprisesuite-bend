# Generated by Django 5.0.6 on 2024-05-29 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='contract',
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
        migrations.DeleteModel(
            name='Milestone',
        ),
    ]
