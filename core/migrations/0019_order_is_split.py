# Generated by Django 5.2.1 on 2025-05-15 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_restockrequest_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_split',
            field=models.BooleanField(default=False),
        ),
    ]
