from django.db import models

# Create your models here.


class WeatherStation(models.Model):
    station_name = models.CharField(max_length=100, null=True, unique=True)

    def __hash__(self):
        return hash(self.station_name)


class WeatherRecord(models.Model):
    station = models.ForeignKey(
        WeatherStation, on_delete=models.CASCADE, related_name="weather_records"
    )
    date = models.DateField(null=False)
    max_temperature = models.FloatField(null=True)
    min_temperature = models.FloatField(null=True)
    # Precipitation in milliliters
    precipitation = models.FloatField(null=True)

    class Meta:
        unique_together = ("station", "date")


class WeatherStatistic(models.Model):
    station = models.ForeignKey(
        WeatherStation,
        on_delete=models.CASCADE,
        related_name="weather_statistics",
    )
    year = models.PositiveSmallIntegerField(null=False)
    avg_max_temperature = models.FloatField(null=True)
    avg_min_temperature = models.FloatField(null=True)
    # Sum in cm
    total_precipitation = models.FloatField(null=True)

    class Meta:
        unique_together = ("station", "year")
