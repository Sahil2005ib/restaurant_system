# Generated by Django 5.2.1 on 2025-05-13 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_salesreport_staffrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('unit', models.CharField(max_length=20)),
                ('restock_approved', models.BooleanField(default=False)),
            ],
        ),
    ]
