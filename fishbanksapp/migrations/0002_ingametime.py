# Generated by Django 5.1.5 on 2025-02-27 17:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fishbanksapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InGameTime",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.FloatField(default=0)),
                ("game_start_time", models.FloatField(default=0)),
                ("time_scale", models.FloatField(default=365.0)),
            ],
        ),
    ]
