# Generated by Django 5.1.5 on 2025-01-29 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "weather",
            "0005_rename_avg_max_temp_weatherstatistic_avg_max_temperature_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="weatherstatistic",
            old_name="avg_precipitation",
            new_name="total_precipitation",
        ),
    ]
