# Generated by Django 5.1.5 on 2025-01-28 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0004_rename_weatherstatistics_weatherstatistic_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="weatherstatistic",
            old_name="avg_max_temp",
            new_name="avg_max_temperature",
        ),
        migrations.RenameField(
            model_name="weatherstatistic",
            old_name="avg_min_temp",
            new_name="avg_min_temperature",
        ),
    ]
