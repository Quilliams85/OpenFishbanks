# Generated by Django 5.1.5 on 2025-03-26 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("fishbanksapp", "0015_rename_organization_invitation_group"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="type",
        ),
        migrations.AddField(
            model_name="transaction",
            name="content_type",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="transaction",
            name="object_id",
            field=models.PositiveIntegerField(default=None),
        ),
        migrations.AddField(
            model_name="transaction",
            name="transaction_type",
            field=models.CharField(
                choices=[
                    ("P2P", "Player to Player"),
                    ("S2P", "Store to Player"),
                    ("P2S", "Player to Store"),
                    ("OTH", "Other"),
                ],
                default="P2P",
                max_length=3,
            ),
        ),
    ]
