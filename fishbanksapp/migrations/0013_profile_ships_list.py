# Generated by Django 5.1.5 on 2025-02-16 19:44

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fishbanksapp", "0012_remove_profile_ships_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="ships_list",
            field=models.JSONField(
                default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder
            ),
        ),
    ]
