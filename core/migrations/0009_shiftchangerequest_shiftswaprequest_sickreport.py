# Generated by Django 5.2 on 2025-05-08 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_feedback_is_urgent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftChangeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_shift', models.CharField(max_length=100)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.staff')),
            ],
        ),
        migrations.CreateModel(
            name='ShiftSwapRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swap_requests', to='core.staff')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swap_targets', to='core.staff')),
            ],
        ),
        migrations.CreateModel(
            name='SickReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reported', models.DateField(auto_now_add=True)),
                ('sick_date', models.DateField()),
                ('status', models.CharField(default='pending', max_length=20)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.staff')),
            ],
        ),
    ]
