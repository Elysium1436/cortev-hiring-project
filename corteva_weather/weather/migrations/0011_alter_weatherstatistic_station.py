# Generated by Django 5.1.5 on 2025-01-30 01:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0010_alter_weatherstatistic_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weatherstatistic",
            name="station",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="weather_statistics",
                to="weather.weatherstation",
            ),
        ),
    ]
