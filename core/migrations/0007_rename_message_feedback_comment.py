# Generated by Django 5.2 on 2025-05-07 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_report'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='message',
            new_name='comment',
        ),
    ]
