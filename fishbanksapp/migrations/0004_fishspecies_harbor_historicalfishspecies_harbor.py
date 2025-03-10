# Generated by Django 5.1.5 on 2025-03-09 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fishbanksapp", "0003_fishspecies_weight_historicalfishspecies_weight"),
    ]

    operations = [
        migrations.AddField(
            model_name="fishspecies",
            name="harbor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="fish",
                to="fishbanksapp.harbor",
            ),
        ),
        migrations.AddField(
            model_name="historicalfishspecies",
            name="harbor",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="fishbanksapp.harbor",
            ),
        ),
    ]
