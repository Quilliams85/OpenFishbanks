# Generated by Django 5.1.5 on 2025-02-12 21:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fishbanksapp", "0005_fishstock"),
    ]

    operations = [
        migrations.AddField(
            model_name="ship",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
