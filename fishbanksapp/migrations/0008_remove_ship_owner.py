# Generated by Django 5.1.5 on 2025-02-12 22:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("fishbanksapp", "0007_rename_fish_capacity_ship_fishing_rate"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ship",
            name="owner",
        ),
    ]
