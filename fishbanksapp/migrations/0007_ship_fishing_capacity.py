# Generated by Django 5.1.5 on 2025-03-03 22:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fishbanksapp", "0006_invoice_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="ship",
            name="fishing_capacity",
            field=models.IntegerField(default=0),
        ),
    ]
